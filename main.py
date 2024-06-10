import multiprocessing
import os
import random
import threading
import time
from datetime import datetime, timezone

import psutil
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import database

app = FastAPI(root_path="/api")

register_tortoise(
    app,
    config=database.TORTOISE_ORM,
    add_exception_handlers=True,
)


@app.get("/")
async def root() -> dict:
    return {
        "message": "Hello World",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


cpu_usage = 0


def update_cpu_usage(interval: float = 3.0) -> None:
    global cpu_usage
    while True:
        usage = psutil.cpu_percent(interval)
        cpu_usage = usage


cpu_monitoring_thread = threading.Thread(target=update_cpu_usage)
cpu_monitoring_thread.daemon = True  # to ensure it exits when the process exits
cpu_monitoring_thread.start()


@app.get("/health")
async def health() -> dict:
    return {
        "cpu_usage": cpu_usage,
        "memory": psutil.virtual_memory()._asdict(),
        "swap": psutil.swap_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "load_avg": psutil.getloadavg(),
        "uptime": time.time() - psutil.boot_time(),
        "network": psutil.net_io_counters()._asdict(),
        "active_processes": len(psutil.pids()),
        "active_threads": sum([len(p.threads()) for p in psutil.process_iter()]),
        "id": {"process": os.getpid(), "thread": threading.get_native_id()},
    }


@app.get("/stress")
async def stress(duration: float = 15.0) -> dict:
    def cpu_intensive_wait(duration: float) -> int:
        stop_at = time.perf_counter() + duration

        result = 0
        while time.perf_counter() < stop_at:
            big = sum(2**i for i in range(random.randint(10, 100)))
            result += big
            result %= 1_000_000

        return result

    proc = multiprocessing.Process(target=cpu_intensive_wait, args=(duration,))
    proc.start()

    return {
        "message": f"A new process has spawned and will block for {duration} second(s).",
        "process_id": proc.pid,
    }
