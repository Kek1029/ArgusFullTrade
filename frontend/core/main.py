import logging
import os
import json
import uvicorn
import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel
from env_config import get_config

config = get_config()
PORT = config["FRONTEND_CORE_PORT"]
RABBITMQ_URL = config["RABBITMQ_GLOBAL_URL"]

app = FastAPI()

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/frontend.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)

class RequestData(BaseModel):
    to: int
    data: dict

# RabbitMQ connection (global)
rabbit_connection = None
rabbit_channel = None
exchange = None

@app.on_event("startup")
async def startup():
    global rabbit_connection, rabbit_channel, exchange
    rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    rabbit_channel = await rabbit_connection.channel()
    exchange = await rabbit_channel.declare_exchange(
        "events",
        aio_pika.ExchangeType.DIRECT,
        durable=True
    )
    logging.info("Connected to RabbitMQ Global")

@app.on_event("shutdown")
async def shutdown():
    await rabbit_connection.close()
    logging.info("RabbitMQ connection closed")

@app.post("/route")
async def route(req: RequestData):
    try:
        payload = json.dumps(req.dict()).encode("utf-8")
        message = aio_pika.Message(
            body=payload,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        routing_key = "route.middleware"
        await exchange.publish(message, routing_key=routing_key)
        logging.info(f"Published to {routing_key}: {payload}")
        return {"status": "OK", "detail": "Message published"}
    except Exception as e:
        logging.error(f"Publish error: {e}")
        return {"status": "ERROR", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
