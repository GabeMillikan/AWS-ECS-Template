import os
import threading
import time

import psutil

from backend.app import app

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


__all__ = ["health"]
