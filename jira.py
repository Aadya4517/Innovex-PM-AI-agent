import os
import requests
from datetime import datetime

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


def fetch_jira_issues():
    if not JIRA_BASE_URL:
        return [
            {
                "id": "PM-1",
                "title": "Login API",
                "status": "In Progress",
                "due_date": "2026-01-12"
            },
            {
                "id": "PM-2",
                "title": "Dashboard UI",
                "status": "Delayed",
                "due_date": "2026-01-08"
            }
        ]

    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    response = requests.get(
        url,
        auth=auth,
        params={"jql": f"project={JIRA_PROJECT_KEY}"},
        headers={"Accept": "application/json"}
    )

    issues = response.json().get("issues", [])
    tasks = []

    for issue in issues:
        f = issue["fields"]
        tasks.append({
            "id": issue["key"],
            "title": f["summary"],
            "status": f["status"]["name"],
            "due_date": f.get("duedate")
        })

    return tasks
