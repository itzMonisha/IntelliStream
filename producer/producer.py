import logging
from kafka import KafkaProducer
import json
import random
import time

logging.basicConfig(
    filename="logs/producer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Producer Started...")

while True:

    event = {
        "animal_id": random.randint(1, 100),
        "temperature": round(random.uniform(37, 42), 2),
        "heart_rate": random.randint(60, 140)
    }

    # Send event to Kafka topic
    producer.send("sensor-events", event)

    # Force immediate delivery during testing
    producer.flush()

    print("Produced:", event)
    logging.info(f"Produced Event: {event}")

    time.sleep(2)
