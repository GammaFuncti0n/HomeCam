import time
import requests
from datetime import datetime

CAMERA_URL = "http://camera_service:8000/snapshot"

INTERVAL_SECONDS = 60 * 60  # раз в 10 секунд


def take_snapshot():
    try:
        resp = requests.post(CAMERA_URL, timeout=30)
        data = resp.json()

        print(f"[{datetime.utcnow().isoformat()}] snapshot:", data)

    except Exception as e:
        print(f"ERROR: Snapshot failed: {e}")


def main():
    print("Scheduler started")

    while True:
        take_snapshot()
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()