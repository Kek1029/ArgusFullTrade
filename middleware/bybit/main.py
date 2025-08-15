import uvicorn
from fastapi import FastAPI
from pybit.unified_trading import HTTP
from pydantic import BaseModel
from typing import Dict, Any


config = get_config()

API_KEY = config["BYBIT_API_KEY"]
API_SECRET = config["BYBIT_API_SECRET"]

session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

info = session.get_account_info()

HOST = config["MIDDLEWARE_INTERNAL_BYBIT_IP"]
PORT = config["MIDDLEWARE_BYBIT_PORT"]

app = FastAPI()

class RequestData(BaseModel):
    source: str
    data: Dict[str, Any]

@app.post("/route")
async def route(req: RequestData):
    try:
        symbol = req.data.get("symbol")
        side = req.data.get("side")
        redis_cache = req.data.get("redis_cache")
        meta = req.data.get("meta")

        return {"status": "OK", "meta": meta}
    except Exception as e:
        logging.error(f"Bybit error: {e}")
        return {"statis": "ERROR", "detail": str(e)}

# ─────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)