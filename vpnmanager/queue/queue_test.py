import pytest
from main import NatsQueue


@pytest.mark.asyncio
async def test_send_queue():
    nats_uri = "nats://localhost:4222"
    nats = NatsQueue(nats_uri)
    await nats.connect()
    q = "requests"
    await nats.publish(q, b'Hello World')


