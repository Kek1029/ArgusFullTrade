import os

def get_config():
    return {
        "BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "FRONTEND_CORE_PORT": int(os.getenv("FRONTEND_CORE_PORT", "6459")),
        "RABBITMQ_GLOBAL_URL": os.getenv("RABBITMQ_GLOBAL_URL", "amqp://guest:guest@rabbitmq-global:5672/"),
        "RABBITMQ_LOCAL_URL": os.getenv("RABBITMQ_LOCAL_URL", "amqp://guest:guest@rabbitmq-local:5672/"),
    }
