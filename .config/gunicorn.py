import os

workers = (os.cpu_count() or 1) * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
