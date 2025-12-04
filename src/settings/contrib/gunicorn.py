"""Gunicorn configuration for the Django application."""

# Binding
bind = "0.0.0.0:8000"

# Worker processes
workers = 1
worker_class = "sync"  # Default sync worker for WSGI applications

# Timeouts
timeout = 60
graceful_timeout = 30
keep_alive = 5  # Keep-alive timeout

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s %({X-Request-ID}i)s'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Miscellaneous
capture_output = True
enable_stdio_inheritance = True


# Specify reasons for closing connections
def on_starting(server) -> None:  # noqa
    """Called just before the master process is initialized."""
    server.log.info("Starting Gunicorn server")


def on_exit(server) -> None:  # noqa
    server.log.info("Shutting down Gunicorn server")


def worker_int(worker) -> None:  # noqa
    worker.log.info("Worker received INT signal")


def worker_abort(worker) -> None:  # noqa
    worker.log.info("Worker received SIGABRT signal")


def worker_exit(server, worker) -> None:  # noqa
    server.log.info(f"Worker exiting (pid: {worker.pid})")
