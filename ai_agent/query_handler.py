def handle_query(query, tasks):
    query = query.lower()

    if "delayed" in query:
        return [t for t in tasks if t["status"] == "Delayed"]

    if "completed" in query:
        return [t for t in tasks if t["status"] == "Completed"]

    if "in progress" in query:
        return [t for t in tasks if t["status"] == "In Progress"]

    return "Sorry, I couldn’t understand the query."

def smart_query(query, tasks):
    q = query.lower()

    if "deadline" in q or "due" in q:
        return "Checking deadlines..."

    if "risk" in q:
        return "Analyzing project risk..."

    if "standup" in q:
        return "Generating daily stand-up..."

    return "🤖 AI Agent: Please rephrase your request."