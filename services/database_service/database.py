import os
import time
import hashlib
import logging
import sys

import requests
import schedule
import re


# ---------------- LOGGING ----------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("database.log", encoding="utf-8")
    ]
)


# ---------------- CONFIG ----------------
LOCAL_FOLDER = "../data"
REMOTE_FOLDER = "/homecam"

STATE_FILE = "uploaded_hashes.txt"

API_BASE = "https://cloud-api.yandex.net/v1/disk/resources"


headers = {
    "Authorization": f"OAuth {os.getenv("YANDEX_TOKEN")}"
}


# ---------------- STATE (HASHES) ----------------

def load_uploaded_hashes():
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())


def save_uploaded_hash(file_hash: str):
    with open(STATE_FILE, "a") as f:
        f.write(file_hash + "\n")


# ---------------- HASHING ----------------

def get_file_hash(path, chunk_size=1024 * 1024):
    """SHA256 hash по содержимому файла"""
    sha = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha.update(chunk)

    return sha.hexdigest()


# ---------------- YANDEX API ----------------

def ensure_folder(path: str):
    """Создать папку (если уже есть — ок)"""
    url = API_BASE
    params = {"path": path}

    resp = requests.put(url, headers=headers, params=params)

    if resp.status_code not in (201, 409):
        resp.raise_for_status()


def get_upload_link(remote_path: str):
    url = f"{API_BASE}/upload"
    params = {
        "path": remote_path,
        "overwrite": "true"
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()

    return resp.json()["href"]


def upload_file(local_path: str, remote_path: str):
    upload_url = get_upload_link(remote_path)

    with open(local_path, "rb") as f:
        resp = requests.put(upload_url, data=f)

    resp.raise_for_status()


# ---------------- CORE LOGIC ----------------

def upload_new_files():
    logging.info("Начало синхронизации...")

    if not os.path.exists(LOCAL_FOLDER):
        logging.warning(f"Папка {LOCAL_FOLDER} не найдена")
        return

    uploaded_hashes = load_uploaded_hashes()

    try:
        ensure_folder(REMOTE_FOLDER)

        for filename in os.listdir(LOCAL_FOLDER):
            local_path = os.path.join(LOCAL_FOLDER, filename)

            if not os.path.isfile(local_path):
                continue

            file_hash = get_file_hash(local_path)

            # уже загружали это содержимое
            if file_hash in uploaded_hashes:
                continue

            remote_path = f"{REMOTE_FOLDER}/{filename}"

            try:
                logging.info(f"Upload: {filename}")

                upload_file(local_path, remote_path)

                save_uploaded_hash(file_hash)

                logging.info(f"Uploaded: {filename}")

            except Exception as e:
                logging.error(f"Failed {filename}: {e}")

        logging.info("Синхронизация завершена")

    except Exception as e:
        logging.error(f"Fatal error: {e}")

def sanitize_filename(name: str) -> str:
    # заменяем опасные символы для Яндекс.Диска
    return re.sub(r'[:\s]', '_', name)

# ---------------- SCHEDULER ----------------

# schedule.every(10).minutes.do(upload_new_files)
schedule.every().hour.do(upload_new_files)

if __name__ == "__main__":
    logging.info("Yandex Disk uploader started")

    upload_new_files()

    while True:
        schedule.run_pending()
        time.sleep(1)