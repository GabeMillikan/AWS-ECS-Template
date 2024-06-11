import os

DB_CONNECTION_STRING = os.getenv(
    "DB_CONNECTION_STRING",
    "postgres://username:password@postgresql:5432/database",
)

TORTOISE_ORM = {
    "connections": {
        "default": DB_CONNECTION_STRING,
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
