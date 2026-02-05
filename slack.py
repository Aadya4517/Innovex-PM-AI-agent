import os
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

def send_slack_message(text: str):
    if not SLACK_WEBHOOK:
        print("⚠ Slack disabled (SLACK_WEBHOOK not set)")
        print(text)
        return

    try:
        requests.post(
            SLACK_WEBHOOK,
            json={"text": text},
            timeout=5
        )
    except Exception as e:
        print("❌ Slack send failed:", e)
