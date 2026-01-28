# gunicorn_config.py
bind = "0.0.0.0:8080"
workers = 2
threads = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "-"
errorlog = "-"
loglevel = "info"
