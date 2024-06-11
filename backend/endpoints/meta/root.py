from datetime import datetime, timezone

from backend.app import app


@app.get("/")
async def root() -> dict:
    return {
        "message": "Hello World",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


__all__ = ["root"]
