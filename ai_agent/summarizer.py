"""
summarizer.py
AI module to summarize project task status
"""
def summarize_tasks(tasks):
    total = len(tasks)
    completed = len([t for t in tasks if t["status"] == "Completed"])
    in_progress = len([t for t in tasks if t["status"] == "In Progress"])
    delayed = len([t for t in tasks if t["status"] == "Delayed"])

    summary = f"""
📊 Project Status Summary

* Total Tasks: {total}
* Completed: {completed}
* In Progress: {in_progress}
* Delayed: {delayed}

⚠️ Attention Required: {delayed} task(s) are delayed.
"""
    return summary