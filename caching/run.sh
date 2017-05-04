uwsgi --enable-threads --http-socket 172.17.0.1:5000 --wsgi-file manager.py --callable api --logto 127.0.0.1:1717
