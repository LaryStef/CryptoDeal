# import multiprocessing


bind = "127.0.0.1:8000"
worker_class = "sync"
# workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "run:app"
reload = True
spew = True
backlog = 1024
timeout = 360
