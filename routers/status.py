from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/status-summary")
def status_summary():
    with open("tasks.json") as f:
        tasks = json.load(f)
    return {"total_tasks": len(tasks), "tasks": tasks}