from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
import aiohttp
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

class BrokerMessage(BaseModel):
    type: str
    payload: Dict[str, Any]
    meta: Optional[Dict[str, str]] = None

class LocalNetAPI:
    def __init__(self, ip: str, port: int, local_ips: list):
        self.app = FastAPI()
        self.ip = ip
        self.port = port
        self.local_ips = local_ips
        self._register_routes()

    def _register_routes(self):
        @self.app.post("/route")
        async def route(msg: BrokerMessage):
            logging.info(f"Received message: {msg.type} → payload: {msg.payload}")

            to_index = msg.payload.get("to")
            if to_index is None:
                logging.warning("Missing 'to' in payload")
                return {"error": "Missing 'to'"}

            try:
                target_ip = self.local_ips[to_index]
                await self.forward_message(target_ip, msg)
                return {"status": "forwarded", "to": target_ip}
            except IndexError:
                logging.error(f"Invalid 'to' index: {to_index}")
                return {"error": "Invalid 'to' index"}

    async def forward_message(self, target_ip: str, msg: BrokerMessage):
        url = f"http://{target_ip}/route"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=msg.dict()) as resp:
                if resp.status == 200:
                    logging.info(f"Message forwarded to {target_ip}")
                else:
                    logging.error(f"Failed to forward to {target_ip}: {resp.status}")

    def run(self):
        uvicorn.run(self.app, host=self.ip, port=self.port)
