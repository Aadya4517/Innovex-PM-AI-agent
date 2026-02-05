from datetime import datetime

def score_priority(task):
    deadline = task.get("due_date")
    status_days = task.get("days_in_status", 0)

    if not deadline:
        return "Low"

    today = datetime.utcnow().date()
    due = datetime.strptime(deadline, "%Y-%m-%d").date()
    days_left = (due - today).days

    if days_left < 0 or status_days >= 5:
        return "High"
    elif days_left <= 2 or status_days >= 3:
        return "Medium"
    else:
        return "Low"
