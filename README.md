# Scheduler Service

Сервис для шкедулера.

До compose запуск происходит так:


## Docker Build

```bash
docker build -t scheduler_service .
```

## Docker Run

```bash
docker run -d -it --name scheduler_service --network homecam_net -v $(pwd):/app scheduler_service
```