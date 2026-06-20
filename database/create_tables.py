from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String
)
import os

engine = create_engine(
    os.getenv("DATABASE_URL", "https://intellistream-2.onrender.com"))

metadata = MetaData()

sensor_events = Table(
    "sensor_events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("animal_id", Integer),
    Column("temperature", Float),
    Column("heart_rate", Integer),
    Column("risk_level", String(20))
)

metadata.create_all(engine)

print("Table created successfully.")
