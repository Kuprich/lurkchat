import logging
from aiogram import Bot, Dispatcher
import asyncio

from handlers import anon_chat
from data.repository import DbRepository

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config.TOKEN)
dp = Dispatcher()
db = DbRepository(config.DB_URL)

dp.include_routers(anon_chat.router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
