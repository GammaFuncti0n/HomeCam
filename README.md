Проект домашней камеры которая делай снимки и видео по запросу.

Докер билд:

docker build -t home_cam .

Докер ран:

docker run -d -it --name home_cam --device=/dev/video0:/dev/video0 --restart unless-stopped --env-file .env --network host -v $(pwd):/workspace home_cam