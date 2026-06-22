import time
from concurrent.futures import ThreadPoolExecutor

events = list(range(50))


def process_event(event):

    time.sleep(1)


start = time.time()

with ThreadPoolExecutor(
    max_workers=3
) as executor:

    executor.map(
        process_event,
        events
    )

end = time.time()

print(
    f"Processed {len(events)} events"
)

print(
    f"Total Time: {round(end-start, 2)} sec"
)
