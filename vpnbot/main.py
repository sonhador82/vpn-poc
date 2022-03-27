import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage, SendChatAction
from aiogram.utils.executor import start_webhook

logging.basicConfig(level=logging.INFO)

bot_logger = logging.getLogger('bot')
bot_logger.setLevel(level=logging.DEBUG)

BOT_TOKEN = os.environ['BOT_TOKEN']
WEBHOOK_HOST='https://92f0-178-66-131-10.ngrok.io'
WEBHOOK_PATH='/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

NATS_URI="nats://localhost:4222"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["welcome"])
async def welcome(message: types.Message):
    welcome_text = '''
        Привет, всем любителям запрещенки.
        Для организации доступа к Instagram, введи /make_vpn
    '''
    return SendMessage(message.chat.id, welcome_text)


@dp.message_handler(commands=["make_vpn"])
async def make_vpn(message: types.Message):
    logging.info(message)
    logging.info(f'make vpn for: {message.from_user.username}, {message.from_user.first_name}, {message.from_user.id}, {message.date}')
    return SendMessage(message.chat.id, "Подготавливаем конфигурацию...")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start



async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path='/',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=8000,
    )