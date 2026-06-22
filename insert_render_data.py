from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://intellistream_1_postgress_user:dg8iIlWtkRRrAUWN8O2NLz2ThVarmZW6@dpg-d8rbfomgvqtc73ertcv0-a.virginia-postgres.render.com/intellistream_1_postgress"
)

with engine.connect() as conn:
    conn.execute(text("""
        INSERT INTO sensor_events
        (animal_id, temperature, heart_rate, risk_level)
        VALUES
        (1,39.5,80,'NORMAL'),
        (2,41.2,120,'HIGH'),
        (3,38.8,75,'NORMAL'),
        (4,42.1,130,'HIGH')
    """))
    conn.commit()

print("Inserted Successfully")
