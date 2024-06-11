import os

CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING",
    "username:password@postgresql:5432/database",
)
CONNECTION_URL = f"postgresql+asyncpg://{CONNECTION_STRING}"


__all__ = ["CONNECTION_URL"]
