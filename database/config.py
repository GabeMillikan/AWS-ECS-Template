TORTOISE_ORM = {
    "connections": {
        "default": "postgresql://dev:insecure-local-only@dev:5432/dev",  # todo pull from ENV
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
