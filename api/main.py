
import json
import logging
from fastapi import FastAPI
from sqlalchemy import text

from api.database import engine
from api.cache import redis_client

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()


@app.get("/")
def home():

    logging.info("Home endpoint accessed")

    return {
        "project": "IntelliStream",
        "status": "running"
    }


@app.get("/events")
def get_events():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM sensor_events")
        )

        rows = []

        for row in result:
            rows.append(
                {
                    "id": row.id,
                    "animal_id": row.animal_id,
                    "temperature": row.temperature,
                    "heart_rate": row.heart_rate,
                    "risk_level": row.risk_level
                }
            )

        logging.info(
            f"Returned {len(rows)} events"
        )

        return rows


@app.get("/high-risk")
def high_risk():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM sensor_events
            WHERE risk_level = 'HIGH'
            """)
        )

        rows = []

        for row in result:
            rows.append(
                {
                    "id": row.id,
                    "animal_id": row.animal_id,
                    "temperature": row.temperature,
                    "heart_rate": row.heart_rate,
                    "risk_level": row.risk_level
                }
            )

        logging.info(
            f"Returned {len(rows)} high-risk events"
        )

        return rows


@app.get("/animal/{animal_id}")
def animal_history(animal_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM sensor_events
            WHERE animal_id = :animal_id
            ORDER BY id DESC
            """),
            {"animal_id": animal_id}
        )

        rows = []

        for row in result:
            rows.append(
                {
                    "id": row.id,
                    "animal_id": row.animal_id,
                    "temperature": row.temperature,
                    "heart_rate": row.heart_rate,
                    "risk_level": row.risk_level
                }
            )

        logging.info(
            f"Animal history requested for Animal ID {animal_id}"
        )

        return rows


@app.get("/stats")
def stats():

    cached = redis_client.get("stats")

    if cached:

        logging.info(
            "Stats served from Redis cache"
        )

        return json.loads(cached)

    with engine.connect() as conn:

        total = conn.execute(
            text("SELECT COUNT(*) FROM sensor_events")
        ).scalar()

        high = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM sensor_events
            WHERE risk_level = 'HIGH'
            """)
        ).scalar()

        normal = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM sensor_events
            WHERE risk_level = 'NORMAL'
            """)
        ).scalar()

        data = {
            "total_events": total,
            "high_risk_events": high,
            "normal_events": normal
        }

        redis_client.setex(
            "stats",
            30,
            json.dumps(data)
        )

        logging.info(
            f"Stats generated from PostgreSQL: {data}"
        )

        return data


@app.get("/latest")
def latest():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM sensor_events
            ORDER BY id DESC
            LIMIT 20
            """)
        )

        rows = []

        for row in result:
            rows.append(
                {
                    "id": row.id,
                    "animal_id": row.animal_id,
                    "temperature": row.temperature,
                    "heart_rate": row.heart_rate,
                    "risk_level": row.risk_level
                }
            )

        logging.info(
            f"Returned latest {len(rows)} events"
        )

        return rows
