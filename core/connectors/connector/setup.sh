apt-get update
apt-get install python-pip
apt-get install docker-engine
apt-get install docker.io
pip install falcon
pip install uwsgi
pip install docker
uwsgi --enable-threads --http-socket 0.0.0.0:10036 --wsgi-file connector.py --callable api
