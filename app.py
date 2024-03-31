import os

from fastapi import FastAPI

app = FastAPI(root_path="/api")

try:
    cors_localhost_port = int(os.getenv("CORS_LOCALHOST_PORT", -1))
except ValueError:
    pass
else:
    if cors_localhost_port > 0:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=[f"http://localhost:{cors_localhost_port}"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

__all__ = ["app"]
