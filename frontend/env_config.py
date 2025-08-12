import os

def get_config():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "FASTAPI_PORT": int(os.getenv("FASTAPI_PORT", "8000")),
        "MIDDLEWARE_PORT": int(os.getenv("MIDDLEWARE_PORT", "8080")),
    }