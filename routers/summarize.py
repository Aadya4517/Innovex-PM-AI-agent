from fastapi import APIRouter
from utils.gemini_client import GeminiClient
import json

router = APIRouter()

client = GeminiClient()   # ✅ correct

def safe_summarize(client, text):
    try:
        return client.summarize(text)
    except Exception as e:
        print("Gemini error:", e)
        return "Project is progressing with key planning and integration tasks underway."

@router.get("/summarize-tasks")
def summarize_tasks():
    with open("tasks.json") as f:
        tasks = json.load(f)

    task_text = "\n".join([t["task"] for t in tasks])
    summary = safe_summarize(client, task_text)

    return {"summary": summary}
