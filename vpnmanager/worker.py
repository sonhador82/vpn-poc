import os
import asyncio
import logging

import nats
from nats.aio.msg import Msg

from client import Client
from vpnservice import get_vpn_service
from botservice import BotService


#logging.basicConfig(level=logging.DEBUG)
BOT_TOKEN = os.environ['BOT_TOKEN']
NATS_URI="nats://127.0.0.1:4222"
NATS_SUBJ="requests"
DAYS=1

async def handler(msg: Msg):
    client: Client = Client.decode(msg.data)
    print(client.first_name, client.tg_user_id)
    vpn = get_vpn_service()
    vpn.issue_access_for(client, DAYS)
    client_cfg = vpn.get_settings_for(client)
    bs = BotService(BOT_TOKEN)
    await bs.send_msg_to(client, client_cfg)


async def main():
    n = await nats.connect(NATS_URI)
    sub = await n.subscribe(NATS_SUBJ, cb=handler)

    client = Client(365848986, "Sonhador")
    await n.publish(NATS_SUBJ, client.encode())

    while True:
        await asyncio.sleep(5)
    await sub.unsubscribe()
 

if __name__ == '__main__':
    asyncio.run(main(), debug=True)