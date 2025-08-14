import multiprocessing

bind = "0.0.0.0:8088"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "*"
proxy_protocol = False
