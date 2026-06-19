import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.pkl"
)

print("Loading model from:", MODEL_PATH)

model = joblib.load(MODEL_PATH)


def predict_risk(temperature, heart_rate):

    data = pd.DataFrame([{
        "temperature": temperature,
        "heart_rate": heart_rate
    }])

    prediction = model.predict(data)

    if prediction[0] == -1:
        return "HIGH"

    return "NORMAL"
