from sqlalchemy import create_engine, text
import os
import logging

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:admin123@127.0.0.1:5432/intellistream"
)

engine = create_engine(DATABASE_URL)


def save_event(animal_id, temperature, heart_rate, risk_level):

    try:

        logging.info(
            f"Inserting Animal ID={animal_id}"
        )

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

        logging.info(
            f"Inserted Animal ID={animal_id}"
        )

    except Exception as e:

        logging.error(
            f"Database Error: {e}"
        )
