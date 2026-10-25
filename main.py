import os
import json
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from threading import Event, Thread
from uuid import uuid4
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import joblib
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

load_dotenv()

from ai_agent.jira import fetch_jira_issues
from jira import add_jira_comment
from slack import send_slack_message
from ai_agent.standup import generate_standup
from priority import score_priority
from summarizer import summarize_tasks
from utils.gemini_client import GeminiClient

app = FastAPI()
LOCAL_TASKS_FILE = Path(__file__).with_name("local_tasks.json")
MODEL_FILE = Path(__file__).with_name("delay_model.pkl")
_scheduler_thread = None
_scheduler_stop = Event()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DelayRiskRequest(BaseModel):
    estimated_days: float
    actual_days: float


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: str = "Not Started"
    due_date: str | None = None


class DelayForecastRequest(BaseModel):
    estimated_days: float = Field(gt=0)
    priority: int = Field(ge=1, le=5)
    dependencies: int = Field(ge=0, le=100)
    team_size: int = Field(ge=1, le=100)


class ProjectQueryRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)


def load_local_tasks():
    if not LOCAL_TASKS_FILE.exists():
        return []
    return json.loads(LOCAL_TASKS_FILE.read_text(encoding="utf-8"))


def get_dashboard_tasks():
    tasks = fetch_jira_issues() + load_local_tasks()
    for task in tasks:
        if task.get("created_at") and task.get("status", "").lower() in {"in progress", "blocked", "delayed"}:
            try:
                created = datetime.fromisoformat(task["created_at"])
                task["days_in_status"] = max(0, (datetime.now() - created).days)
            except ValueError:
                pass
        task["priority"] = score_priority(task)
    return tasks


def summarize_project(tasks):
    fallback = summarize_tasks(tasks)
    if not os.getenv("GEMINI_API_KEY"):
        return fallback, "rules"
    try:
        return GeminiClient().summarize(tasks), "gemini"
    except Exception as exc:
        print(f"Gemini summary unavailable ({type(exc).__name__}); using rules fallback")
        return fallback, "rules_fallback"


def find_deadline_alerts(tasks):
    today = datetime.now().date()
    alerts = []
    done_statuses = {"completed", "done", "resolved", "closed"}
    for task in tasks:
        status = task.get("status", "").lower()
        due_date = task.get("due_date")
        if status in done_statuses:
            continue
        reasons = []
        if due_date:
            try:
                due = datetime.strptime(due_date, "%Y-%m-%d").date()
                if due < today:
                    reasons.append(f"overdue since {due_date}")
                elif due <= today + timedelta(days=7):
                    reasons.append(f"due by {due_date}")
            except ValueError:
                pass
        if status in {"delayed", "blocked", "overdue"}:
            reasons.append(f"status is {task.get('status')}")
        if status in {"in progress", "blocked", "delayed"} and task.get("days_in_status", 0) >= 5:
            reasons.append(f"unchanged for {task['days_in_status']} days")
        if reasons:
            alerts.append({"task": task, "reasons": reasons})
    return alerts


@lru_cache(maxsize=1)
def load_delay_model():
    if not MODEL_FILE.exists():
        raise RuntimeError("delay_model.pkl is missing; run python train_model.py to create it")
    return joblib.load(MODEL_FILE)


def run_daily_slack_digest():
    tasks = get_dashboard_tasks()
    summary, _ = summarize_project(tasks)
    alerts = find_deadline_alerts(tasks)
    if alerts:
        summary += "\n\nAlerts:\n" + "\n".join(
            f"- {item['task']['id']} {item['task']['title']}: {', '.join(item['reasons'])}"
            for item in alerts
        )
    try:
        result = send_slack_message(summary)
        print(f"Daily Slack digest: {'sent' if result['sent'] else result['reason']}")
    except Exception as exc:
        print(f"Daily Slack digest failed ({type(exc).__name__})")


@app.on_event("startup")
def start_daily_slack_digest():
    global _scheduler_thread, _scheduler_stop
    enabled = os.getenv("DAILY_SLACK_REPORT_ENABLED", "false").lower() == "true"
    if not enabled:
        return
    if not os.getenv("SLACK_WEBHOOK"):
        print("Daily Slack digest not started: configure SLACK_WEBHOOK")
        return
    try:
        ZoneInfo(os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata"))
    except ZoneInfoNotFoundError:
        print("Daily Slack digest not started: SCHEDULER_TIMEZONE is invalid")
        return
    _scheduler_stop = Event()
    def daily_loop():
        timezone = ZoneInfo(os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata"))
        while not _scheduler_stop.is_set():
            now = datetime.now(timezone)
            next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            if _scheduler_stop.wait((next_run - now).total_seconds()):
                return
            try:
                run_daily_slack_digest()
            except Exception as exc:
                print(f"Daily Slack digest failed ({type(exc).__name__})")
    _scheduler_thread = Thread(target=daily_loop, name="daily-slack-digest", daemon=True)
    _scheduler_thread.start()


@app.on_event("shutdown")
def stop_daily_slack_digest():
    _scheduler_stop.set()
    if _scheduler_thread and _scheduler_thread.is_alive():
        _scheduler_thread.join(timeout=1)


@app.post("/tasks", status_code=201)
def create_task(request: TaskCreateRequest):
    title = request.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Task title cannot be blank")
    if request.due_date:
        try:
            datetime.strptime(request.due_date, "%Y-%m-%d")
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Due date must use YYYY-MM-DD") from exc

    task = {
        "id": f"LOCAL-{uuid4().hex[:8].upper()}",
        "title": title,
        "status": request.status,
        "due_date": request.due_date,
        "days_in_status": 0,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks = load_local_tasks()
    tasks.append(task)
    LOCAL_TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    task["priority"] = score_priority(task)
    return task


@app.get("/")
def home():
    return {"message": "PM AI Agent API is running", "docs": "/docs", "dashboard": "/dashboard"}

@app.get("/dashboard")
def dashboard():
    tasks = get_dashboard_tasks()

    completed = [t for t in tasks if t["status"].lower() in {"completed", "done", "resolved", "closed"}]
    in_progress = [t for t in tasks if "progress" in t["status"].lower()]
    delayed = [t for t in tasks if t["status"].lower() in {"delayed", "blocked", "overdue"}]

    summary, summary_source = summarize_project(tasks)
    return {
        "counts": {
            "completed": len(completed),
            "in_progress": len(in_progress),
            "delayed": len(delayed),
            "total": len(tasks)
        },
        "tasks": tasks,
        "summary": summary,
        "summary_source": summary_source,
        "standup": generate_standup(tasks)
    }

@app.get("/deadline-risk")
def deadline_risk():
    today = datetime.today().date()
    warning = []
    overdue = []
    for task in get_dashboard_tasks():
        due_date = task.get("due_date")
        if not due_date or task["status"].lower() in {"completed", "done", "resolved", "closed"}:
            continue
        due = datetime.strptime(due_date, "%Y-%m-%d").date()
        if due < today:
            overdue.append(task)
        elif (due - today).days <= 7:
            warning.append(task)
    return {
        "warning": len(warning),
        "overdue": len(overdue),
        "warning_tasks": warning,
        "overdue_tasks": overdue
    }

@app.post("/delay-risk")
def delay_risk(request: DelayRiskRequest):
    if request.estimated_days <= 0 or request.actual_days < 0:
        raise HTTPException(status_code=422, detail="Estimated days must be positive and actual days cannot be negative")

    overrun = max(0, request.actual_days - request.estimated_days)
    risk_percent = min(100, round((overrun / request.estimated_days) * 100))
    if risk_percent > 70:
        risk = "High Risk"
    elif risk_percent > 0:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"
    explanation = (
        f"Actual duration is {overrun:g} day(s) over estimate."
        if overrun
        else "Actual duration is within the estimate."
    )
    return {"risk": risk, "risk_percent": risk_percent, "explanation": explanation}


@app.post("/delay-forecast")
def delay_forecast(request: DelayForecastRequest):
    try:
        model = load_delay_model()
        features = pd.DataFrame([{
            "estimated_days": request.estimated_days,
            "priority": request.priority,
            "dependencies": request.dependencies,
            "team_size": request.team_size,
        }])
        probability = round(float(model.predict_proba(features)[0][1]) * 100, 2)
    except Exception as exc:
        print(f"Delay model unavailable ({type(exc).__name__})")
        raise HTTPException(status_code=503, detail="Delay model is unavailable; check Python ML dependencies and delay_model.pkl") from exc
    level = "High Risk" if probability >= 70 else "Medium Risk" if probability >= 40 else "Low Risk"
    return {
        "risk_percent": probability,
        "risk": level,
        "model": "LogisticRegression",
        "note": "Demo model trained on a small sample dataset; use as a signal, not a guarantee.",
    }


@app.post("/query")
def project_query(request: ProjectQueryRequest):
    tasks = get_dashboard_tasks()
    if os.getenv("GEMINI_API_KEY"):
        try:
            return {"answer": GeminiClient().answer(request.query, tasks), "source": "gemini"}
        except Exception as exc:
            print(f"Gemini query unavailable ({type(exc).__name__}); using local query handling")
    query = request.query.lower()
    statuses = {
        "delayed": {"delayed", "blocked", "overdue"},
        "completed": {"completed", "done", "resolved", "closed"},
        "in progress": {"in progress"},
    }
    for phrase, values in statuses.items():
        if phrase in query or (phrase == "delayed" and "block" in query):
            matches = [task for task in tasks if task.get("status", "").lower() in values]
            answer = ", ".join(task["title"] for task in matches) if matches else "No matching tasks."
            return {"answer": answer, "source": "local rules"}
    if "deadline" in query or "due" in query or "overdue" in query:
        alerts = find_deadline_alerts(tasks)
        answer = ", ".join(item["task"]["title"] for item in alerts) if alerts else "No upcoming deadline alerts."
        return {"answer": answer, "source": "local rules"}
    return {"answer": "Add a Gemini API key for general project questions. I can answer status and deadline questions with local rules.", "source": "local rules"}


@app.get("/integrations/status")
def integrations_status():
    return {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "jira": bool(os.getenv("JIRA_BASE_URL") and os.getenv("JIRA_EMAIL") and os.getenv("JIRA_API_TOKEN") and os.getenv("JIRA_PROJECT_KEY")),
        "slack": bool(os.getenv("SLACK_WEBHOOK")),
        "delay_model": MODEL_FILE.exists(),
        "daily_slack_digest": os.getenv("DAILY_SLACK_REPORT_ENABLED", "false").lower() == "true" and bool(os.getenv("SLACK_WEBHOOK")),
    }


@app.post("/alerts/send")
def send_project_alerts():
    tasks = get_dashboard_tasks()
    alerts = find_deadline_alerts(tasks)
    if not alerts:
        message = "PM AI Agent: no overdue, near-deadline, delayed, blocked, or stuck tasks found."
    else:
        lines = ["PM AI Agent project alerts:"]
        for item in alerts:
            task = item["task"]
            lines.append(f"• {task['id']} — {task['title']}: {', '.join(item['reasons'])}")
        message = "\n".join(lines)
    try:
        slack_result = send_slack_message(message)
    except Exception as exc:
        slack_result = {"sent": False, "reason": f"Slack request failed ({type(exc).__name__})"}
    jira_results = []
    jira_is_configured = all(os.getenv(name) for name in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_PROJECT_KEY"))
    if jira_is_configured:
        for item in alerts:
            task = item["task"]
            if not str(task.get("id", "")).startswith("LOCAL-"):
                try:
                    comment_id = add_jira_comment(task["id"], f"PM AI Agent alert: {', '.join(item['reasons'])}.")
                    jira_results.append({"issue": task["id"], "sent": True, "comment_id": comment_id})
                except Exception as exc:
                    jira_results.append({"issue": task["id"], "sent": False, "reason": type(exc).__name__})
    return {
        "alert_count": len(alerts),
        "slack": slack_result,
        "jira_comments": jira_results,
        "message": message,
    }

@app.post("/pm-report")
def generate_pm_report():
    tasks = get_dashboard_tasks()
    today = datetime.today().date()

    completed = []
    in_progress = []
    delayed = []
    pending = []
    overdue = []
    completed_statuses = {"completed", "done", "resolved", "closed"}
    delayed_statuses = {"delayed", "blocked", "overdue"}

    for t in tasks:
        status = t["status"].lower()

        if status in completed_statuses:
            completed.append(t)
        elif "progress" in status:
            in_progress.append(t)
        elif status in delayed_statuses:
            delayed.append(t)
        else:
            pending.append(t)

        if t.get("due_date"):
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if due < today and status not in completed_statuses:
                overdue.append(t)

    report_text = f"""
📊 *PM Sprint Report*

• Total Tasks: {len(tasks)}
• Completed: {len(completed)}
• In Progress: {len(in_progress)}
• Delayed: {len(delayed)}
• Pending: {len(pending)}

⚠️ *Overdue Tasks*
{chr(10).join([f"- {t['id']} {t['title']}" for t in overdue]) or "None 🎉"}
"""

    try:
        slack_result = send_slack_message(report_text)
    except Exception as exc:
        slack_result = {"sent": False, "reason": f"Slack request failed ({type(exc).__name__})"}

    return {
        "total_tasks": len(tasks),
        "completed": len(completed),
        "in_progress": len(in_progress),
        "delayed": len(delayed),
        "pending": len(pending),
        "high_risk_tasks": overdue,
        "slack": slack_result,
    }
