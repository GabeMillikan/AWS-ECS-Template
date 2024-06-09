import asyncio
import time
from datetime import datetime, timezone

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


@app.get("/health")
async def health() -> dict:
    return {"todo": "include more information here"}


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
