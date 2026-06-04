import subprocess
from fastapi import FastAPI
from datetime import datetime
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("camera.log", encoding="utf-8")]
)

app = FastAPI()

OUT_DIR = Path("/data")
OUT_DIR.mkdir(exist_ok=True)

DEVICE = "/dev/video0"  # USB cam (или /dev/video10 для CSI через v4l2loopback)

@app.get("/sanity_check")
def check_available():
    '''Check if service is available'''
    logging.info("Check status")
    return {"status": "available"}

@app.post("/snapshot")
def snapshot():
    '''
    Method for take one snapshot and save it in filename
    '''
    filename = OUT_DIR / f"snapshot_{datetime.utcnow().isoformat()}.jpg"

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "v4l2",
        "-video_size", "1280x720", #"1280x720" "1920x1080"
        "-i", DEVICE,
        "-frames:v", "5",
        str(filename)
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logging.info(f"Take snapshot: {filename} with size {format_size(Path(filename).stat().st_size)}")
    return {
        "file": str(filename),
        "exists": filename.exists()
    }

@app.post("/video")
def record_video(duration: int = 5):
    '''
    Method for record video with selected duration (default 5 sec)
    '''
    filename = OUT_DIR / f"video_{datetime.utcnow().isoformat()}.mp4"

    cmd = [
        "ffmpeg",
        "-y",

        # input
        "-f", "v4l2",
        "-input_format", "mjpeg",
        "-video_size", "960x540",
        "-framerate", "30",
        "-i", DEVICE,

        # duration
        "-t", str(duration),

        # encoding
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",

        str(filename)
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    logging.info(f"Take video: {filename} with size {format_size(Path(filename).stat().st_size)}")
    return {
        "file": str(filename),
        "duration": duration,
        "exists": filename.exists()
    }

def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.2f} GB"