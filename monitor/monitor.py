import os

def selfLocation():
	return os.path.dirname(os.path.realpath(__file__))

def start():
    uwsgi = "uwsgi --enable-threads --http-socket 127.0.0.1:10036 --wsgi-file " + selfLocation() + "/pages/main.py --callable api"
    os.system(uwsgi)
