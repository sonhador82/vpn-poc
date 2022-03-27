import random
import uuid
import datetime
import json
import asyncio

import aioredis


async def main():
    """Scan command example."""
    redis = aioredis.from_url("redis://localhost", decode_responses=True)

    # data = {}
    # for i in range(1, 100, 10):
    #     client = str(uuid.uuid4())
    #     dt = datetime.datetime.now()
    #     dt += datetime.timedelta(seconds=i)
    #     await redis.hset(client, "ts_exit", str(dt))   
  
    #await redis.mset(data)
    async with redis.client() as conn:
        cur = b"0"  # set initial cursor to 0
        while cur:
            cur, keys = await conn.scan(cur, match="*")
            for k in keys:              
                data = await conn.hgetall(k)
                time_to_close = datetime.datetime.fromisoformat(data["ts_exit"])
                print(data["ts_exit"], time_to_close)
                cur_time = datetime.datetime.now()
                if cur_time > time_to_close:
                    print(f'Close: {k}')

if __name__ == "__main__":
    import os

    if "redis_version:2.6" not in os.environ.get("REDIS_VERSION", ""):
        asyncio.run(main())