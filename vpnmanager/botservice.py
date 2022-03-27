import logging
import os
from aiogram import Bot, Dispatcher, types

from client import Client


class BotService:
    def __init__(self, bot_token) -> None:
        self.bot = Bot(token=bot_token)
 
    async def send_msg_to(self, client: Client, msg: str):
        try:
            msg = await self.bot.send_message(client.tg_user_id, msg)
        finally:
            await self.bot.close()
        print(client.tg_user_id)
        print(msg)
        logging.debug(msg)
