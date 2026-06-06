# IoT Plant Monitoring & Irrigation System (Edge Distributed Architecture)

A fault-tolerant, distributed IoT system designed for autonomous monitoring and control of a home plant irrigation setup during long-term absence.

The system runs on a Raspberry Pi 5 and is built as a multi-service Dockerized architecture with emphasis on reliability, offline tolerance, and independent service failure isolation.

---

## Motivation

This project was built to solve a practical real-world problem:

> How do you reliably monitor and control a home irrigation system while being away for several weeks, under unstable connectivity conditions?

Instead of a monolithic script, the system was designed as a **distributed edge architecture** with explicit failure handling, offline resilience, and cloud synchronization.

---

## System Overview

The system is deployed on a Raspberry Pi 5 and consists of independent services orchestrated via Docker Compose.

Each service is isolated to ensure that **failure in one component does not bring down the entire system**.

### High-level architecture:

* Camera Service (FastAPI)
* Telegram Bot Service (control interface)
* Scheduler Service (autonomous fallback automation)
* Cloud Sync Service (Yandex Disk integration)

---

## Architecture Principles

This system was designed with production-grade engineering constraints in mind:

* **Service Isolation**: each component runs in its own container
* **Fault Tolerance**: independent restart policies (`restart unless stopped`)
* **Offline-first design**: system remains functional without Telegram connectivity
* **Graceful degradation**: scheduler ensures continued operation if bot fails
* **Secure access control**: user whitelisting for bot interactions
* **Observability**: structured logging per service
* **Edge deployment**: optimized for Raspberry Pi environment
* **Cloud synchronization**: eventual consistency with remote storage

---

## Services

### Camera Service (FastAPI)

Responsible for image/video capture from connected camera module.

**Responsibilities:**

* Accepts HTTP requests to capture images or videos
* Stores media locally with timestamped filenames
* Returns file metadata to calling services
* Logs capture events (file name, size, timestamp)

---

### Telegram Bot Service

Primary user-facing control interface.

**Responsibilities:**

* Accepts commands only from authenticated users (`auth.yaml`)
* Rejects and logs unauthorized access attempts
* Sends capture requests to Camera Service via FastAPI
* Returns captured media to users via Telegram
* Operates behind a proxy due to network restrictions

**Security design:**

* User whitelist authentication
* Suspicious activity logging (unauthorized access attempts)

---

### Scheduler Service (Fallback Automation Layer)

Ensures system continues operating even if external interfaces fail.

**Responsibilities:**

* Periodically triggers camera captures (hourly)
* Guarantees continuous data collection without Telegram dependency
* Acts as system fallback if bot or proxy becomes unavailable

---

### Cloud Sync Service (Yandex Disk Integration)

Handles persistent off-device backup and synchronization.

**Responsibilities:**

* Syncs captured files to Yandex Disk every 2 hours
* Uses hash-based deduplication to avoid redundant uploads
* Maintains local record of uploaded files (`uploaded_hashes.txt`)
* Ensures eventual consistency between edge device and cloud storage

---

## Fault Tolerance Design

The system is designed around partial failure tolerance:

* If **Telegram bot fails** → scheduler continues capturing data
* If **scheduler fails** → bot remains functional for manual control
* If **cloud sync fails** → local data remains intact
* If **network fails** → system continues local operation
* If **power is lost** → Raspberry Pi auto-restarts services on recovery

Docker restart policies ensure automatic recovery of all services.

---

## Observability

Each service maintains its own logs:

* Camera: capture events, file metadata
* Bot: user interactions, command logs, unauthorized access attempts
* Scheduler: execution timestamps
* Cloud sync: upload events, deduplication results

Logs are stored locally per service for post-analysis.

---

## Security Model

* Telegram bot uses strict whitelist authentication (`auth.yaml`)
* Unknown users are ignored and logged as suspicious activity
* API access between services is internal (Docker network)
* External access is only via Telegram interface

---

## Configuration

### Root environment variables (`.env` in project root)

Required for Telegram Bot:

```
TG_TOKEN=your_token_here
```

---

### Cloud Sync Service environment (`services/sync_service/.env`)

Required for Yandex Disk integration:

```
YANDEX_TOKEN=your_token_here
```

---

## Project Structure

```
.
├── auth.yaml
├── compose.yaml
├── data/
├── services
│   ├── bot_service
│   ├── camera_service
│   ├── database_service
│   └── scheduler_service
└── README.md
```

---

## Deployment

System is fully containerized and deployed via Docker Compose:

```bash
docker compose up -d --build
```

All services are automatically restarted unless explicitly stopped.

---

## Key Engineering Characteristics

* Distributed system design (multi-service architecture)
* Edge computing (Raspberry Pi deployment)
* Fault isolation between services
* Offline-first operational model
* Event-driven interaction between services
* External API integration (Telegram, Yandex Disk)
* Hash-based deduplication for cloud sync
* System-level thinking (failure modes explicitly modeled)

---

## Notes

* This system was intentionally designed and tested under real-world conditions (multi-week unattended operation scenario).
* It prioritizes reliability and autonomy over complexity.
* All components are intentionally decoupled to maximize survivability under partial system failure.

---

## Summary

This project demonstrates:

* Practical distributed systems design on edge hardware
* Production-style thinking (failure modes, monitoring, isolation)
* Multi-service ML/IoT-style architecture
* Autonomous system design under constrained connectivity