import logging
import asyncio
from aiogram import (
    Bot,
    Dispatcher,
    types,
)
from aiogram.filters.command import Command
from aiogram.client.default import DefaultBotProperties
from routers import router
from core.settings import settings

bot = Bot(
    token=settings.bot.token,
    default=DefaultBotProperties(parse_mode=settings.bot.default_parse_mode),
)

dp = Dispatcher()

dp.include_router(router=router)

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
