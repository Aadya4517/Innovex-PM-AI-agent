from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routers import status, summarize, deadline, alerts

app = FastAPI(title="PM AI Agent Backend")

app.include_router(status.router)
app.include_router(summarize.router)
app.include_router(deadline.router)
app.include_router(alerts.router)

@app.get("/")
def root():
    return {"message": "Backend is running"}