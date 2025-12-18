def generate_standup(tasks):
    yesterday = []
    today = []
    blockers = []

    for task in tasks:
        if task["status"].lower() == "completed":
            yesterday.append(task["title"])
        elif task["status"].lower() == "in progress":
            today.append(task["title"])
        elif task["status"].lower() == "delayed":
            blockers.append(task["title"])

    response = "🧑‍💻 DAILY STANDUP UPDATE\n\n"

    response += "✅ Yesterday:\n"
    response += "\n".join(f"- {t}" for t in yesterday) if yesterday else "- No completed tasks"

    response += "\n\n🚀 Today:\n"
    response += "\n".join(f"- {t}" for t in today) if today else "- No tasks in progress"

    response += "\n\n⚠️ Blockers:\n"
    response += "\n".join(f"- {t}" for t in blockers) if blockers else "- No blockers"

    return response