'''from fastapi import APIRouter
import json
from datetime import datetime

router = APIRouter()

@router.get("/deadline-check")
def deadline_check():
    with open("tasks.json") as f:
        tasks = json.load(f)
    near_deadline = [t for t in tasks if datetime.strptime(t["deadline"], "%Y-%m-%d") <= datetime.now()]
    return {"near_deadline_tasks": near_deadline}

'''

from fastapi import APIRouter
import json
from datetime import datetime, timedelta
import os

router = APIRouter()

@router.get("/deadline-check")
def deadline_check():
    # Make sure path is correct
    file_path = os.path.join(os.getcwd(), "tasks.json")

    with open(file_path) as f:
        tasks = json.load(f)

    now = datetime.now()
    threshold = now + timedelta(days=2)

    near_deadline = []

    for t in tasks:
        try:
            deadline_date = datetime.strptime(t["deadline"], "%Y-%m-%d")
            if now <= deadline_date <= threshold:
                near_deadline.append(t)
        except Exception as e:
            print("Date parsing error:", e, "for task:", t)

    return {
        "now": now.strftime("%Y-%m-%d"),
        "threshold": threshold.strftime("%Y-%m-%d"),
        "near_deadline_tasks": near_deadline
    }
