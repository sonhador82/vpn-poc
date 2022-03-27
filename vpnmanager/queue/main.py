import nats
from nats.aio.client import Client


class NatsQueue:
    def __init__(self, uri: str):
        self.uri = uri
        self.conn: Client = None

    async def connect(self):
        self.conn = await nats.connect(self.uri)

    async def publish(self, queue: str, data: bytes):
        await self.conn.publish(queue, data)
