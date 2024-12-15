from aiogram import Dispatcher, Router, Bot
from aiogram.enums import ParseMode
from handlers import register_all_handlers
from tortoise import Tortoise
from config import API_TOKEN, init_db
import logging
import asyncio




async def main():
    await init_db()
    try:
        bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        register_all_handlers(dp)
        await dp.start_polling(bot)
    finally:
        await Tortoise.close_connections()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", )
    asyncio.run(main())