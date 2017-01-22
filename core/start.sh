apt-get update && echo 'y' | sudo apt-get upgrade
uwsgi --enable-threads --http-socket 0.0.0.0:10036 --wsgi-file controller.py --callable api