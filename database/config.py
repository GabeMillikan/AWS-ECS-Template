import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgresql:5432")
POSTGRES_AUTH = os.getenv("POSTGRES_AUTH", "username:password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "database")

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{POSTGRES_AUTH}@{POSTGRES_HOST}/{POSTGRES_DB}",
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
