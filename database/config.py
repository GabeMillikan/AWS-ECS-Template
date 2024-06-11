import os

CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING",
    "dev:insecure-local-only@database:5432/dev",
)
CONNECTION_URL = f"postgresql+asyncpg://{CONNECTION_STRING}"


__all__ = ["CONNECTION_URL"]
