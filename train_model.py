# Note: actual_days is used only to label delay, not as a feature

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("tasks.csv")

# Select features and target
X = data[['estimated_days', 'priority', 'dependencies', 'team_size']]
y = data['is_delayed']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "delay_model.pkl")
print("Model saved as delay_model.pkl")
