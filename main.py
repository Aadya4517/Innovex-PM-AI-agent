from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from ai_agent.jira import fetch_jira_issues
from ai_agent.slack import send_slack_message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dashboard")
def dashboard():
    tasks = fetch_jira_issues()

    completed = len([t for t in tasks if t["status"].lower() == "completed"])
    in_progress = len([t for t in tasks if "progress" in t["status"].lower()])
    delayed = len([t for t in tasks if t["status"].lower() == "delayed"])

    return {
        "counts": {
            "completed": completed,
            "in_progress": in_progress,
            "delayed": delayed
        }
    }

@app.post("/pm-report")
def generate_pm_report():
    tasks = fetch_jira_issues()
    today = datetime.today().date()

    completed = []
    in_progress = []
    delayed = []
    overdue = []

    for t in tasks:
        status = t["status"].lower()

        if status == "completed":
            completed.append(t)
        elif "progress" in status:
            in_progress.append(t)
        else:
            delayed.append(t)

        if t.get("due_date"):
            due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if due < today and status != "completed":
                overdue.append(t)

    report_text = f"""
📊 *PM Sprint Report*

• Total Tasks: {len(tasks)}
• Completed: {len(completed)}
• In Progress: {len(in_progress)}
• Delayed: {len(delayed)}

⚠️ *Overdue Tasks*
{chr(10).join([f"- {t['id']} {t['title']}" for t in overdue]) or "None 🎉"}
"""

    send_slack_message(report_text)

    return {
        "total_tasks": len(tasks),
        "completed": len(completed),
        "in_progress": len(in_progress),
        "delayed": len(delayed),
        "high_risk_tasks": overdue
    }
