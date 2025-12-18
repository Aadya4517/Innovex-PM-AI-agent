from summarizer import summarize_tasks
from standup import generate_standup
from deadline_tracker import track_deadlines
from risk_predictor import predict_project_risk
from alerts import generate_alerts

def ai_project_report(tasks):
    return {
        "summary": summarize_tasks(tasks),
        "standup": generate_standup(tasks),
        "deadlines": track_deadlines(tasks),
        "risk": predict_project_risk(tasks),
        "alerts": generate_alerts(tasks)
    }