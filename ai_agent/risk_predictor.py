def predict_project_risk(tasks):
    delayed = len([t for t in tasks if t["status"] == "Delayed"])
    total = len(tasks)

    if delayed / total > 0.3:
        return "🔴 High Risk: Many tasks are delayed"
    elif delayed > 0:
        return "🟠 Medium Risk: Some delays detected"
    else:
        return "🟢 Low Risk: Project is healthy"