import os
from datetime import datetime, timezone

import requests

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")


def fetch_jira_issues():
    if not JIRA_BASE_URL:
        return [
            {"id": "PM-1", "title": "Login API", "status": "In Progress", "due_date": "2026-01-12", "days_in_status": 0},
            {"id": "PM-2", "title": "Dashboard UI", "status": "Delayed", "due_date": "2026-01-08", "days_in_status": 0},
        ]
    if not all((JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY)):
        raise RuntimeError("Jira is configured incompletely; set email, API token, and project key")

    response = requests.get(
        f"{JIRA_BASE_URL}/rest/api/3/search/jql",
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        params={
            "jql": f"project={JIRA_PROJECT_KEY} ORDER BY updated DESC",
            "fields": "summary,status,duedate,created,statuscategorychangedate",
            "expand": "changelog",
            "maxResults": 100,
        },
        headers={"Accept": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    tasks = []
    for issue in response.json().get("issues", []):
        fields = issue["fields"]
        status_since = fields.get("statuscategorychangedate") or fields.get("created")
        for history in issue.get("changelog", {}).get("histories", []):
            if any(item.get("field", "").lower() == "status" for item in history.get("items", [])):
                status_since = history.get("created") or status_since
        try:
            changed = datetime.fromisoformat(status_since.replace("Z", "+00:00"))
            if changed.tzinfo is None:
                changed = changed.replace(tzinfo=timezone.utc)
            days_in_status = max(0, (datetime.now(timezone.utc) - changed).days)
        except (AttributeError, TypeError, ValueError):
            days_in_status = 0
        tasks.append({
            "id": issue["key"],
            "title": fields["summary"],
            "status": fields["status"]["name"],
            "due_date": fields.get("duedate"),
            "days_in_status": days_in_status,
        })
    return tasks


def add_jira_comment(issue_key: str, message: str):
    """Post an alert as a Jira issue comment."""
    if not all((JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN)):
        raise RuntimeError("Jira URL, email, and API token are required to post comments")
    response = requests.post(
        f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment",
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": message}],
                }],
            }
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("id")
