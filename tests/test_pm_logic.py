from datetime import datetime, timedelta

import pytest

from main import DelayRiskRequest, delay_risk, find_deadline_alerts
from priority import score_priority
from summarizer import summarize_tasks


def test_priority_is_low_without_deadline():
    assert score_priority({}) == "Low"


def test_priority_is_high_for_overdue_task():
    yesterday = (datetime.utcnow().date() - timedelta(days=1)).isoformat()
    assert score_priority({"due_date": yesterday}) == "High"


def test_priority_is_medium_when_due_within_two_days():
    soon = (datetime.utcnow().date() + timedelta(days=2)).isoformat()
    assert score_priority({"due_date": soon}) == "Medium"


def test_priority_is_high_for_task_stuck_five_days():
    future = (datetime.utcnow().date() + timedelta(days=30)).isoformat()
    assert score_priority({"due_date": future, "days_in_status": 5}) == "High"


def test_summary_counts_task_statuses():
    result = summarize_tasks([
        {"status": "Completed"},
        {"status": "In Progress"},
        {"status": "Delayed"},
        {"status": "Not Started"},
    ])
    assert "Completed: 1" in result
    assert "In Progress: 1" in result
    assert "Delayed: 1" in result


def test_alerts_include_task_due_within_seven_days():
    due_date = (datetime.now().date() + timedelta(days=3)).isoformat()
    alerts = find_deadline_alerts([{"id": "KAN-1", "status": "To Do", "due_date": due_date}])
    assert [item["task"]["id"] for item in alerts] == ["KAN-1"]


def test_alerts_exclude_task_due_after_seven_days():
    due_date = (datetime.now().date() + timedelta(days=8)).isoformat()
    alerts = find_deadline_alerts([{"id": "KAN-1", "status": "To Do", "due_date": due_date}])
    assert alerts == []


def test_alerts_include_blocked_task_without_due_date():
    alerts = find_deadline_alerts([{"id": "KAN-2", "status": "Blocked"}])
    assert [item["task"]["id"] for item in alerts] == ["KAN-2"]


def test_alerts_skip_completed_tasks():
    due_date = (datetime.now().date() + timedelta(days=1)).isoformat()
    alerts = find_deadline_alerts([{"id": "KAN-3", "status": "Done", "due_date": due_date}])
    assert alerts == []


@pytest.mark.parametrize(
    ("actual_days", "expected_risk", "expected_percent"),
    [(10, "Low Risk", 0), (12, "Medium Risk", 20), (18, "High Risk", 80)],
)
def test_delay_risk_levels(actual_days, expected_risk, expected_percent):
    result = delay_risk(DelayRiskRequest(estimated_days=10, actual_days=actual_days))
    assert result["risk"] == expected_risk
    assert result["risk_percent"] == expected_percent
