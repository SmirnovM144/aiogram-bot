"""
Main entry point for the bot application.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config.settings import Settings
from database import Database
from handlers import callbacks_router, commands_router, setup_database


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main application entry point."""
    # Validate settings
    Settings.validate()

    # Initialize database
    db = Database(Settings.DATABASE_URL)

    logger.info("Connecting to database...")
    await db.connect()
    logger.info("Database connected successfully")

    logger.info("Initializing database tables...")
    await db.init_tables()
    logger.info("Database tables initialized")

    # Setup handlers with database
    setup_database(db)

    # Initialize bot and dispatcher
    bot = Bot(
        token=Settings.BOT_TOKEN,
        default=DefaultBotProperties()
    )

    dp = Dispatcher()

    # Include routers
    dp.include_router(callbacks_router)
    dp.include_router(commands_router)

    logger.info("Starting bot polling...")

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            timeout=60
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        logger.info("Cleaning up resources...")
        await db.close()
        await bot.session.close()
        logger.info("Cleanup completed")


if __name__ == "__main__":
    asyncio.run(main())
