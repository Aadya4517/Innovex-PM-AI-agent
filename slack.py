import os
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

def send_slack_message(text: str):
    if not SLACK_WEBHOOK:
        return {"sent": False, "reason": "SLACK_WEBHOOK is not configured"}

    response = requests.post(SLACK_WEBHOOK, json={"text": text}, timeout=10)
    response.raise_for_status()
    return {"sent": True, "reason": "Slack accepted the message"}
