from fastapi import FastAPI
from ai_agent.summarizer import summarize_tasks

app = FastAPI()

@app.get("/")
def home():
    return {"message": "PM AI Agent Backend Running"}

@app.get("/status-summary")
def status_summary():
    tasks = [
        {"title": "Login API", "status": "Completed"},
        {"title": "Dashboard UI", "status": "Delayed"},
        {"title": "Payment Module", "status": "In Progress"}
    ]

    summary = summarize_tasks(tasks)
    return {"summary": summary}
