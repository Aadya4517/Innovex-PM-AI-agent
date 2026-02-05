def generate_pm_report(tasks):
    completed = []
    in_progress = []
    delayed = []
    high_risk = []

    from datetime import datetime
    today = datetime.utcnow().date()

    for t in tasks:
        status = t["status"].lower()
        due = datetime.fromisoformat(t["due_date"]).date()

        if status == "done":
            completed.append(t)
        elif due < today:
            delayed.append(t)
            high_risk.append(t)
        else:
            in_progress.append(t)

    return {
        "total_tasks": len(tasks),
        "completed": len(completed),
        "in_progress": len(in_progress),
        "delayed": len(delayed),
        "high_risk_tasks": high_risk
    }
