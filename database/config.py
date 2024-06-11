import os

CONNECTION_STRING = os.getenv(
    "DATABASE_CONNECTION_STRING",
    "api:p4ssw0rd@template-guide-database.ctw2u8ywk3i1.us-east-2.rds.amazonaws.com:5432/prod",
)
CONNECTION_URL = f"postgresql+asyncpg://{CONNECTION_STRING}"


__all__ = ["CONNECTION_URL"]
