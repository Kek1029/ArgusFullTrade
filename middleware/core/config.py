import os

class Config:
    def __init__(self):
        self.FRONTEND_CORE_PORT = int(os.getenv("FRONTEND_CORE_PORT", 6459))
        self.FRONTEND_TELEGRAM_PORT = int(os.getenv("FRONTEND_TELEGRAM_PORT", 6541))
        self.FRONTEND_WEB_PORT = int(os.getenv("FRONTEND_WEB_PORT", 5713))
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

        self.MIDDLEWARE_CORE_PORT = int(os.getenv("MIDDLEWARE_CORE_PORT", 6132))
        self.MIDDLEWARE_INTERNAL_IP = os.getenv("MIDDLEWARE_INTERNAL_IP")
        self.MIDDLEWARE_FRONTEND_PORT = int(os.getenv("MIDDLEWARE_FRONTEND_PORT", 6133))
        self.MIDDLEWARE_BACKEND_PORT = int(os.getenv("MIDDLEWARE_BACKEND_PORT", 6134))
        self.MIDDLEWARE_BYBIT_PORT = int(os.getenv("MIDDLEWARE_BYBIT_PORT", 6135))
        self.MIDDLEWARE_REDIS_PORT = int(os.getenv("MIDDLEWARE_REDIS_PORT", 6136))

        self.BACKEND_CORE_PORT = int(os.getenv("BACKEND_CORE_PORT", 6521))
        self.BACKEND_MIDDLEWARE_PORT = int(os.getenv("BACKEND_MIDDLEWARE_PORT", 6522))
        self.BACKEND_REDIS_PORT = int(os.getenv("BACKEND_REDIS_PORT", 6523))

        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
        self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

        self.RABBIT_GLOBAL_URL = os.getenv("RABBITMQ_GLOBAL_URL")
        self.EXCHANGE_NAME = "events"
        self.MIDDLEWARE_QUEUE = "route.middleware"
        self.MIDDLEWARE_ROUTING_KEY = "route.middleware"
        self.FRONTEND_ROUTING_KEY = "order.frontend"
        self.BYBIT_ROUTING_KEY = "order.bybit"
        self.REDIS_ROUTING_KEY = "order.redis"
        self.BACKEND_ROUTING_KEY = "order.backend"

        self.BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
        self.BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

        self.validate()

    def validate(self):
        missing = []
        if not self.REDIS_PASSWORD:
            missing.append("REDIS_PASSWORD")
        if not self.BYBIT_API_KEY or not self.BYBIT_API_SECRET:
            missing.append("BYBIT_API_KEY / BYBIT_API_SECRET")
        if not self.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not self.RABBIT_GLOBAL_URL:
            missing.append("RABBITMQ_GLOBAL_URL")
        if missing:
            raise ValueError(f"Missing config values: {', '.join(missing)}")

    def log_summary(self):
        print("Config loaded:")
        print(f"  Middleware Core Port: {self.MIDDLEWARE_CORE_PORT}")
        print(f"  Redis URL: {self.REDIS_URL}")
        print(f"  RabbitMQ Global: {self.RABBIT_GLOBAL_URL}")
        print(f"  Exchange: {self.EXCHANGE_NAME}")
        print(f"  Bybit Key: {self.BYBIT_API_KEY[:4]}****")
        print(f"  Telegram Token: {self.TELEGRAM_BOT_TOKEN[:4]}****")
