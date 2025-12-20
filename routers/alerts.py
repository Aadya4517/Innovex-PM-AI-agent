'''from fastapi import APIRouter
from slack_sdk import WebClient
from routers.deadline import deadline_check

router = APIRouter()
client = WebClient(token="10176145721761-10176157665537-MJxVOkiyqVg5ji2geJ5XAZRq")

@router.get("/send-alerts")
def send_alerts():
    near_deadline = deadline_check()["near_deadline_tasks"]
    for task in near_deadline:
        client.chat_postMessage(channel="#alerts", text=f"Task '{task['task']}' is near deadline!")
    return {"alerts_sent": len(near_deadline)}

'''

import os
from fastapi import APIRouter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from routers.deadline import deadline_check

router = APIRouter()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#alerts")

if not SLACK_TOKEN:
    raise ValueError("SLACK_TOKEN not set in environment variables")

client = WebClient(token=SLACK_TOKEN)


@router.get("/send-alerts")
def send_alerts():
    result = deadline_check()
    near_deadline = result.get("near_deadline_tasks", [])

    alerts_sent = 0

    for task in near_deadline:
        try:
            client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"⏰ *Deadline Alert*\nTask: *{task['task']}*\nDeadline: {task['deadline']}"
            )
            alerts_sent += 1

        except SlackApiError as e:
            print("Slack error:", e.response["error"])

    return {
        "alerts_sent": alerts_sent,
        "tasks_checked": len(near_deadline)
    }
