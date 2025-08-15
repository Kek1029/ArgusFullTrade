import asyncio
from config import Config
from rabbitAPI import RabbitClient, QueueBinding, BrokerMessage

async def handle_message(msg: BrokerMessage):
    print("📨 Received message:")
    print("Type:", msg.type)
    print("Payload:", msg.payload)
    print("Meta:", msg.meta)

async def main():
    cfg = Config()
    cfg.log_summary()

    client = RabbitClient(cfg.RABBIT_GLOBAL_URL)
    await client.connect()

    binding = QueueBinding(
        exchange=cfg.EXCHANGE_NAME,
        routing_key=cfg.MIDDLEWARE_ROUTING_KEY,
        queue_name=cfg.MIDDLEWARE_QUEUE
    )

    await client.subscribe(binding, handle_message)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
