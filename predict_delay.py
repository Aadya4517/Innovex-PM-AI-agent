import joblib
import pandas as pd

model = joblib.load("delay_model.pkl")

def predict_delay(task_data):
    df = pd.DataFrame([task_data])
    probability = model.predict_proba(df)[0][1]
    return round(probability * 100, 2)

def risk_explanation(level):
    if level == "High Risk":
        return "Task is likely to be delayed due to high dependencies and limited team size."
    elif level == "Medium Risk":
        return "Task may face delays if dependencies are not resolved on time."
    else:
        return "Task is on track with low chances of delay."


def risk_level(risk):
    if risk > 70:
        return "High Risk"
    elif risk > 40:
        return "Medium Risk"
    else:
        return "Low Risk"


# Sample test
sample_task = {
    "estimated_days": 6,
    "priority": 4,
    "dependencies": 3,
    "team_size": 2
}

risk = predict_delay(sample_task)
print(f"Delay Risk: {risk}%")

level = risk_level(risk)
print(f"Delay Risk: {risk}% ({level})")

explanation = risk_explanation(level)
print(f"Delay Risk: {risk}% ({level})")
print("Explanation:", explanation)

