import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from src.settings import settings
from src.bot.handlers.chat import router as main_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout,
    )

    bot = Bot(
        token=settings.telegram_token,
    )

    dp = Dispatcher()

    dp.include_router(main_router)

    try:
        logging.info("Bot started!")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()
        logging.info("Bot stopped!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually")
