import logging

import uvicorn
from aiohttp.web_middlewares import middleware
from fastapi import FastAPI
from pydantic import BaseModel
from env_config import get_config
import httpx

config = get_config()
PORT = config["FRONTEND_CORE_PORT"]

app = FastAPI()

import os
os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename="logs/frontend.log", filemode="w", level=logging.INFO, format="%(asctime)s %(message)s)")

class RequestData(BaseModel):
    to: int
    data: dict

@app.post("/route")
async def route(req: RequestData):
    logging.info(f"Received request: to: {req.to}, data: {req.data}")

    try:
        async with httpx.AsyncClient() as client:
            middleware_port = config["MIDDLEWARE_CORE_PORT"]
            middleware_url = f"http://middleware:{middleware_port}/route"
            response = await client.post(url=middleware_url, json=req.data)
            logging.info(f"Response status: {response.status_code}, body: {response.text}")
            return {
                "status": "OK",
                "middleware_response": response.json()
            }
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {"status": "ERROR", "detail": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
