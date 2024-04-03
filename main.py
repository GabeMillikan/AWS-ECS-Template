from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {
        "message": "Hello World",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
