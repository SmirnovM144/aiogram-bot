from database.db import Database
from handlers.routes import router, setup_database
from dotenv import load_dotenv
from aiohttp import TCPConnector
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
import asyncio
from os import getenv
print("MAIN FILE STARTED")

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
DATABASE_URL = getenv("DATABASE_URL")

db = Database(DATABASE_URL)
setup_database(db)


async def main():
    print("connecting db...")
    await db.connect()
    print("db connected")

    print("init tables...")
    await db.init_tables()
    print("tables ready")

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties()
    )

    dp = Dispatcher()
    dp.include_router(router)

    print("starting polling...")

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
