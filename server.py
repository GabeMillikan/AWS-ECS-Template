from app import app


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World!"}
