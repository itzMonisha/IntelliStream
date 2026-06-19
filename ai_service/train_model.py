import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

print("Generating training data...")

# Generate synthetic livestock sensor data
np.random.seed(42)

data = pd.DataFrame({
    "temperature": np.random.normal(38.5, 0.8, 1000),
    "heart_rate": np.random.normal(90, 15, 1000)
})

print("Training Isolation Forest model...")

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(data)

# Save model
joblib.dump(model, "ai-service/model.pkl")

print("Model trained and saved successfully!")
