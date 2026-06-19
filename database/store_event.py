from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://admin:admin123@127.0.0.1:5432/intellistream"
)


def save_event(animal_id, temperature, heart_rate, risk_level):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO sensor_events
            (animal_id, temperature, heart_rate, risk_level)
            VALUES
            (:animal_id, :temperature, :heart_rate, :risk_level)
            """),
            {
                "animal_id": animal_id,
                "temperature": temperature,
                "heart_rate": heart_rate,
                "risk_level": risk_level
            }
        )

        conn.commit()
