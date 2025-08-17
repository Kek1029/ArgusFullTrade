# main.py
import logging
import os
import asyncio
import uvicorn
import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional
from env_config import get_config

# ─────────────────────────────────────────────
config = get_config()
PORT = config["FRONTEND_CORE_PORT"]

app = FastAPI()

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/frontend.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# ─────────────────────────────────────────────
class RequestData(BaseModel):
    to: int
    data: Dict[str, str]

class BrokerMessage(BaseModel):
    type: str
    payload: RequestData
    meta: Optional[Dict[str, str]] = None

# ─────────────────────────────────────────────
rabbit_connection = None
rabbit_channel = None
exchange = None

async def consume_frontend():
    queue = await rabbit_channel.declare_queue("order.frontend", durable=True)
    await queue.bind(exchange, routing_key="order.frontend")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    data = BrokerMessage.model_validate_json(message.body.decode())
                    logging.info(f"📨 Received in frontend: {data.type} → {data.payload}")
                except Exception as e:
                    logging.error(f"❌ Failed to process frontend message: {e}")

async def connect_rabbit(retries: int = 10, delay: int = 1):
    global rabbit_connection, rabbit_channel, exchange
    for i in range(retries):
        try:
            rabbit_connection = await aio_pika.connect_robust(
                f"amqp://{config['RABBITMQ_USER']}:{config['RABBITMQ_PASS']}@{config['RABBITMQ_HOST']}:{config['RABBITMQ_PORT']}/"
            )
            rabbit_channel = await rabbit_connection.channel()
            exchange = await rabbit_channel.declare_exchange(
                "events",
                aio_pika.ExchangeType.DIRECT,
                durable=True
            )
            logging.info("Connected to RabbitMQ")
            return
        except Exception as e:
            logging.warning(f"RabbitMQ connection failed ({i+1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("Cannot connect to RabbitMQ after multiple retries")

# ─────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    await connect_rabbit()
    asyncio.create_task(consume_frontend())


@app.on_event("shutdown")
async def shutdown():
    if rabbit_connection:
        await rabbit_connection.close()
        logging.info("RabbitMQ connection closed")

# ─────────────────────────────────────────────
@app.post("/route")
async def route(req: BrokerMessage):
    try:
        body = req.model_dump_json().encode("utf-8")

        message = aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        routing_key = "route.middleware"
        await exchange.publish(message, routing_key=routing_key)

        logging.info(f"Published to {routing_key}: {body.decode()}")
        return {"status": "OK", "detail": "Message published"}
    except Exception as e:
        logging.error(f"Publish error: {e}")
        return {"status": "ERROR", "detail": str(e)}

# ─────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
