import multiprocessing
import random
import time

from backend.app import app


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


__all__ = ["stress"]
