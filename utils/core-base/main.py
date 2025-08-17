import asyncio
import logging
import uvicorn
from threading import Thread

from config import Config
from rabbitAPI import RoutingRabbitClient, QueueBinding, BrokerMessage
from localNetAPI import LocalNetAPI

logging.basicConfig(level=logging.INFO)

cfg = Config()
api = LocalNetAPI(ip=cfg.local_ips[1],
                  port=str.split(cfg.local_ips[1], ":")[1],
                  local_ips=cfg.local_ips[1:])
client: RoutingRabbitClient = None

async def handle_message(msg: BrokerMessage):
    logging.info(f"AMQP received: {msg.type}")
    await api.route(msg)

async def run_worker():
    global client
    client = RoutingRabbitClient(cfg.rabbitmq_url, cfg.routing_map)
    await client.connect()

    for routing_key, ip in cfg.routing_map.items():
        queue_name = f"queue.{routing_key.replace('.', '_')}"
        binding = QueueBinding(
            exchange=cfg.exchange_name,
            routing_key=routing_key,
            queue_name=queue_name
        )
        logging.info(f"Binding routing_key '{routing_key}' to IP '{ip}' → queue '{queue_name}'")
        await client.subscribe(binding, handle_message)

    while True:
        await asyncio.sleep(10)

def run_api():
    api.run()

async def main():
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()

    await run_worker()

if __name__ == "__main__":
    asyncio.run(main())
