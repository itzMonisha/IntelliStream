import json
import logging

from fastapi import FastAPI
from sqlalchemy import text

from api.database import engine
from api.cache import redis_client

# ----------------------------------
# Logging Configuration
# ----------------------------------

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

# ----------------------------------
# Home
# ----------------------------------


@app.get("/")
def home():

    logging.info("Home endpoint accessed")

    return {
        "project": "IntelliStream",
        "status": "running"
    }

# ----------------------------------
# All Events
# ----------------------------------


@app.get("/events")
def get_events():

    logging.info("/events endpoint called")

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

# ----------------------------------
# High Risk Events
# ----------------------------------


@app.get("/high-risk")
def high_risk():

    logging.info("/high-risk endpoint called")

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

# ----------------------------------
# Animal History
# ----------------------------------


@app.get("/animal/{animal_id}")
def animal_history(animal_id: int):

    logging.info(
        f"/animal/{animal_id} endpoint called"
    )

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
            f"Returned {len(rows)} records for Animal ID {animal_id}"
        )

        return rows

# ----------------------------------
# Stats (Redis Cache)
# ----------------------------------


@app.get("/stats")
def stats():

    logging.info("/stats endpoint called")

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
            WHERE risk_level='HIGH'
            """)
        ).scalar()

        normal = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM sensor_events
            WHERE risk_level='NORMAL'
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

# ----------------------------------
# Analytics Dashboard
# ----------------------------------


@app.get("/analytics")
def analytics():

    logging.info(
        "/analytics endpoint called"
    )

    with engine.connect() as conn:

        total_events = conn.execute(
            text("SELECT COUNT(*) FROM sensor_events")
        ).scalar()

        high_risk = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM sensor_events
            WHERE risk_level='HIGH'
            """)
        ).scalar()

        avg_temp = conn.execute(
            text("""
            SELECT AVG(temperature)
            FROM sensor_events
            """)
        ).scalar()

        avg_hr = conn.execute(
            text("""
            SELECT AVG(heart_rate)
            FROM sensor_events
            """)
        ).scalar()

        total_animals = conn.execute(
            text("""
            SELECT COUNT(DISTINCT animal_id)
            FROM sensor_events
            """)
        ).scalar()

        high_risk_percent = (
            (high_risk / total_events) * 100
            if total_events > 0
            else 0
        )

        data = {
            "total_events": total_events,
            "total_animals": total_animals,
            "avg_temperature": round(avg_temp, 2) if avg_temp else 0,
            "avg_heart_rate": round(avg_hr, 2) if avg_hr else 0,
            "high_risk_percent": round(high_risk_percent, 2)
        }

        logging.info(
            f"Analytics Generated: {data}"
        )

        return data

# ----------------------------------
# Health Check
# ----------------------------------


@app.get("/health")
def health():

    logging.info(
        "/health endpoint called"
    )

    return {
        "api": "UP",
        "database": "UP",
        "redis": "UP"
    }

# ----------------------------------
# Latest Events
# ----------------------------------


@app.get("/latest")
def latest():

    logging.info(
        "/latest endpoint called"
    )

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


@app.get("/metrics")
def metrics():
    logging.info(
        "/metrics endpoint called"
    )

    with engine.connect() as conn:

        total_events = conn.execute(
            text("SELECT COUNT(*) FROM sensor_events")
        ).scalar()

        high_risk = conn.execute(
            text("""
        SELECT COUNT(*)
        FROM sensor_events
        WHERE risk_level='HIGH'
        """)
        ).scalar()

        normal = conn.execute(
            text("""
        SELECT COUNT(*)
        FROM sensor_events
        WHERE risk_level='NORMAL'
        """)
        ).scalar()

        total_animals = conn.execute(
            text("""
        SELECT COUNT(DISTINCT animal_id)
        FROM sensor_events
        """)
        ).scalar()

        avg_temp = conn.execute(
            text("""
        SELECT AVG(temperature)
        FROM sensor_events
        """)
        ).scalar()

        avg_hr = conn.execute(
            text("""
        SELECT AVG(heart_rate)
        FROM sensor_events
        """)
        ).scalar()

        logging.info(
            f"Metrics Generated: "
            f"Events={total_events}, "
            f"HighRisk={high_risk}"
        )

        return {
            "total_events": total_events,
            "high_risk_events": high_risk,
            "normal_events": normal,
            "total_animals": total_animals,
            "avg_temperature": round(avg_temp, 2) if avg_temp else 0,
            "avg_heart_rate": round(avg_hr, 2) if avg_hr else 0
        }
