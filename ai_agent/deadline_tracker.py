from datetime import datetime

def track_deadlines(tasks):
    today = datetime.today().date()
    overdue = []
    upcoming = []

    for task in tasks:
        due_date = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        if due_date < today and task["status"] != "Completed":
            overdue.append(task["title"])
        elif (due_date - today).days <= 2:
            upcoming.append(task["title"])

    return {
        "overdue": overdue,
        "upcoming": upcoming
    }