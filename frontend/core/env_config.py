# env_config.py
import os

def get_config():
    return {
        "BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "FRONTEND_CORE_PORT": int(os.getenv("FRONTEND_CORE_PORT", "6459")),
        "RABBITMQ_PORT": int(os.getenv("RABBITMQ_PORT", "5672")),
        "RABBITMQ_USER": os.getenv("RABBITMQ_USER", "guest"),
        "RABBITMQ_PASS": os.getenv("RABBITMQ_PASS", "guest"),
        "RABBITMQ_HOST": os.getenv("RABBITMQ_HOST", "rabbitmq"),
        # Optional: Define RABBITMQ_GLOBAL_URL if required, but not necessary for frontend-core
        "RABBITMQ_GLOBAL_URL": os.getenv("RABBITMQ_GLOBAL_URL", "amqp://guest:guest@rabbitmq:5672/")
    }