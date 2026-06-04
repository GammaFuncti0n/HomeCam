FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY camera.py .

RUN mkdir -p /data

CMD ["uvicorn", "camera:app", "--host", "0.0.0.0", "--port", "8000"]