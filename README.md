This is simple script for queueing youtube videos and generating downlaod links them in the background with workers. It supports multi-thread. You can run workey.py multiple times. Works with redis.

Works with Python 2.X

Requirements:
sudo apt-get install youtube-dl
pip install redis
pip install rq

Usage:
python worker.py
python server.py
http://127.0.0.1:8080/GsS0jpLTypg