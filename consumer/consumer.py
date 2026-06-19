from database.store_event import save_event
from kafka import KafkaConsumer
from ai_service.predict import predict_risk
import json
import logging
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


logging.basicConfig(
    filename="logs/consumer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

consumer = KafkaConsumer(
    "sensor-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="sensor-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("📥 Consumer Started...")

for message in consumer:

    event = message.value

    risk = predict_risk(
        event["temperature"],
        event["heart_rate"]
    )

    save_event(
        event["animal_id"],
        event["temperature"],
        event["heart_rate"],
        risk
    )

    print("\n================================")
    print(f"Animal ID   : {event['animal_id']}")
    print(f"Temperature : {event['temperature']}")
    print(f"Heart Rate  : {event['heart_rate']}")
    print(f"Risk Level  : {risk}")
    print("================================")
    print("✅ Saved to PostgreSQL")

    logging.info(
        f"Animal={event['animal_id']} "
        f"Temp={event['temperature']} "
        f"HeartRate={event['heart_rate']} "
        f"Risk={risk}"
    )
