def generate_alerts(tasks):
    alerts = []

    for task in tasks:
        if task["status"] == "Delayed":
            alerts.append(f"⚠️ Task '{task['title']}' is delayed!")

    if not alerts:
        alerts.append("✅ No critical alerts. Project is on track.")

    return alerts