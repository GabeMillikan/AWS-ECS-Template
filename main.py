import asyncio
import time
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {
        "message": "Hello World",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/stress")
async def stress(duration: float = 5.0) -> dict:
    started_at = time.perf_counter()
    n = 0
    while time.perf_counter() - started_at < duration:
        n += 1
        if n % 10_000 == 0:
            await asyncio.sleep(0)

    return {
        "n": n,
        "note": "add a `?duration={seconds}` parameter to increase the delay",
    }
