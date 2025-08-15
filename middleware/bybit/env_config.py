# env_config.py
import os

def get_config():
    return {
        "MIDDLEWARE_INTERNAL_BYBIT_IP": os.getenv("MIDDLEWARE_INTERNAL_BYBIT_IP", "172.21.0.4"),
        "MIDDLEWARE_BYBIT_PORT": int(os.getenv("MIDDLEWARE_BYBIT_PORT", "6135")),
        "BYBIT_API_KEY": os.getenv("BYBIT_API_KEY"),
        "BYBIT_API_SECRET": os.getenv("BYBIT_API_SECRET"),
    }

