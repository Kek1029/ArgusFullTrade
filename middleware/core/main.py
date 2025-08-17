import asyncio
import logging
from config import Config
from rabbitAPI import RabbitClient, QueueBinding, BrokerMessage

logging.basicConfig(level=logging.INFO)

async def handle_message(msg: BrokerMessage):
    logging.info("Received: %s → %s", msg.type, msg.payload)

async def run_worker():
    cfg = Config()
    cfg.log_summary()

    while True:
        try:
            client = RabbitClient(cfg.RABBIT_GLOBAL_URL)
            await client.connect()

            binding = QueueBinding(
                exchange=cfg.EXCHANGE_NAME,
                routing_key=cfg.MIDDLEWARE_ROUTING_KEY,
                queue_name=cfg.MIDDLEWARE_QUEUE
            )

            await client.subscribe(binding, handle_message)

            # Keep alive
            while True:

                await asyncio.sleep(10)

        except Exception as e:
            logging.error(f"Worker error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_worker())
