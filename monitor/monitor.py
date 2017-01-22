import os

def start():
	os.system("uwsgi --enable-threads --http-socket 127.0.0.1:10066 --wsgi-file pages/main.py --callable api")