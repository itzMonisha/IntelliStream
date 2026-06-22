import uuid
from database.store_event import save_event
from kafka import KafkaConsumer
from ai_service.predict import predict_risk


from concurrent.futures import ThreadPoolExecutor
import threading
import json
import logging
import sys
import os
import time

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
CONSUMER_ID = str(uuid.uuid4())[:8]

print(
    f"Consumer Started: {CONSUMER_ID}"
)

# ----------------------------------
# Worker Function
# ----------------------------------


def process_event(event):

    print("STEP 1")

    start = time.time()

    thread_name = threading.current_thread().name

    print("STEP 2")
    logging.info(
        f"Received Event: {event}"
    )
    print(
        f"Consumer {CONSUMER_ID} "
        f"handled Animal {event['animal_id']}"
    )
    risk = predict_risk(
        event["temperature"],
        event["heart_rate"]
    )

    print("STEP 3")

    try:

        save_event(
            event["animal_id"],
            event["temperature"],
            event["heart_rate"],
            risk
        )

        logging.info(
            f"Saved Event {event['animal_id']}"
        )

    except Exception as e:

        logging.error(
            f"Consumer Error: {e}"
        )
    # print("DATABASE SAVE SKIPPED")

    print("STEP 4")

    end = time.time()

    print("\n================================")
    print(f"Thread      : {thread_name}")
    print(f"Animal ID   : {event['animal_id']}")
    print(f"Temperature : {event['temperature']}")
    print(f"Heart Rate  : {event['heart_rate']}")
    print(f"Risk Level  : {risk}")
    print(f"Time Taken  : {round(end-start, 2)} sec")
    print("================================")
    print("✅ Saved to PostgreSQL")

    logging.info(
        f"Thread={thread_name} "
        f"Animal={event['animal_id']} "
        f"Temp={event['temperature']} "
        f"HeartRate={event['heart_rate']} "
        f"Risk={risk}"
    )

# ----------------------------------
# Thread Pool
# ----------------------------------


executor = ThreadPoolExecutor(
    max_workers=3
)

print("📥 Multi-threaded Consumer Started...")

# ----------------------------------
# Kafka Consumer Loop
# ----------------------------------

for message in consumer:

    event = message.value

    executor.submit(
        process_event,
        event
    )
