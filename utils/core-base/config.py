import os
import json

class Config:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_GLOBAL_URL", "amqp://guest:guest@localhost:5672/") \
        self.exchange_name = "events"
        self.local_ips = self._parse_json("LOCAL_IPS")
        self.routing_keys = self._parse_json("RABBITMQ_ROUTING_KEYS")
        self.routing_map = self._build_routing_map()

    def _parse_json(self, var_name, default="[]"):
        try:
            return json.loads(os.getenv(var_name, default))
        except json.JSONDecodeError:
            return []

    def _build_routing_map(self):
        if len(self.local_ips) != len(self.routing_keys):
            raise ValueError("LOCAL_IPS and RABBITMQ_ROUTING_KEYS must be the same length")
        return dict(zip(self.routing_keys, self.local_ips))

