def summarize_tasks(tasks):
    completed = 0
    in_progress = 0
    delayed = 0

    for task in tasks:
        status = task.get("status", "").lower()

        if status == "completed":
            completed += 1
        elif status in ["in progress", "in-progress"]:
            in_progress += 1
        else:
            delayed += 1

    return (
        "📊 *Daily Project Summary*\n\n"
        f"✅ Completed: {completed}\n"
        f"⏳ In Progress: {in_progress}\n"
        f"🚨 Delayed: {delayed}"
    )
