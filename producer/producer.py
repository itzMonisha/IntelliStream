from kafka import KafkaProducer
import json
import random
import time

print("Creating Kafka Producer...")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Kafka Producer Connected")

while True:

    event = {
        "animal_id": random.randint(1, 100),
        "temperature": round(random.uniform(37, 42), 2),
        "heart_rate": random.randint(60, 140)
    }

    print("Before Send")

    future = producer.send(
        "sensor-events",
        event
    )

    print("After Send")

    producer.flush()

    print("After Flush")

    print("Produced:", event)

    time.sleep(2)
