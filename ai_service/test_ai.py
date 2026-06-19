from predict import predict_risk

print(
    predict_risk(
        temperature=42,
        heart_rate=140
    )
)

print(
    predict_risk(
        temperature=38,
        heart_rate=85
    )
)
