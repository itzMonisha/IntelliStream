from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String
)

engine = create_engine(
    "postgresql://intellistream_1_postgress_user:dg8iIlWtkRRrAUWN8O2NLz2ThVarmZW6@dpg-d8rbfomgvqtc73ertcv0-a.virginia-postgres.render.com/intellistream_1_postgress"
)

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

print("Table created successfully")
