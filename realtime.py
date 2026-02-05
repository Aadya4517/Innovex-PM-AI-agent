import time
from datetime import datetime
from ai_agent.jira import fetch_jira_issues
from ai_agent.slack import send_slack_message

def start_realtime_monitor():
    import threading

    def monitor():
        while True:
            tasks = fetch_jira_issues()
            today = datetime.utcnow().date()

            for task in tasks:
                due_date = task.get("due_date")
                status = task.get("status", "").lower()

                if not due_date:
                    continue

                due = datetime.fromisoformat(due_date).date()

                if due < today and status != "completed":
                    send_slack_message(
                        f"🚨 *Overdue Jira Task Alert*\n"
                        f"📌 {task['title']}\n"
                        f"⏰ Due: {due_date}"
                    )

            time.sleep(3600)  # check every hour

    threading.Thread(target=monitor, daemon=True).start()
