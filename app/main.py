import os
import asyncio
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.environ['BOT_TOKEN']


async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )

async def main():
    bot = Bot(token=BOT_TOKEN)

    try:
        msgs = await bot.get_updates()
        print(msgs)

        #msg = await bot.send_message(365848986, "Hello world")
        
    finally:
        await bot.close()
    return


    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler, commands={"start", "restart"})
        await disp.start_polling()
    finally:
        await bot.close()

asyncio.run(main())