import time
import requests
from datetime import datetime
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("scheduler.log", encoding="utf-8")]
)

INTERVAL_SECONDS = 60 * 60  # раз в 1 час

def take_snapshot():
    try:
        resp = requests.post("http://camera_service:8000/snapshot", timeout=10)
        data = resp.json()

        logging.info(f"Take snapshot:", data)

    except Exception as e:
        logging.error(f"ERROR: Snapshot failed: {e}")


def main():
    logging.info("Scheduler started")

    while True:
        take_snapshot()
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()