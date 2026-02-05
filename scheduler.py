from apscheduler.schedulers.background import BackgroundScheduler
from ai_agent.jira import fetch_jira_issues
from ai_agent.summarizer import summarize_tasks
from ai_agent.slack import send_slack_message

def start_scheduler():
    scheduler = BackgroundScheduler()

    def daily_report():
        tasks = fetch_jira_issues()
        summary = summarize_tasks(tasks)
        send_slack_message(summary)

    scheduler.add_job(daily_report, "cron", hour=9, minute=0)
    scheduler.start()
