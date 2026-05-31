from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiohttp import TCPConnector
from dotenv import load_dotenv
from handlers.routes import router, setup_database
from database.db import Database

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
DATABASE_URL = getenv("DATABASE_URL")

db = Database(DATABASE_URL)
setup_database(db)


async def main():
    await db.connect()
    await db.init_tables()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(),
        connector=TCPConnector(
            ssl=False,
            ttl_dns_cache=300,
        )
    )

    dp = Dispatcher()
    dp.include_router(router)

    print("Start..")

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            timeout=60
        )
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
