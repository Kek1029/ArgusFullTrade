import os

def get_config():
    return {
        "BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "FASTAPI_PORT": int(os.getenv("FRONTEND_CORE_PORT", "6459")),
        "MIDDLEWARE_PORT": int(os.getenv("MIDDLEWARE_CORE_PORT", "6132")),
    }