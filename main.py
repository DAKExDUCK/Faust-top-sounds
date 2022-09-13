import asyncio
import os

import dotenv
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from bot.handlers.default import register_handlers_default
from bot.handlers.logger import logger
from bot.handlers.secondary import register_handlers_secondary
from bot.objects import data

dotenv.load_dotenv()


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/get_logfile", description="Получить Logs (admin)"),
    ]
    await bot.set_my_commands(commands)


async def main():
    data.start()
    logger.info("Configuring...")
    
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_default(dp)
    register_handlers_secondary(dp)

    await set_commands(bot)

    await dp.start_polling()
    data.close()


if __name__ == '__main__':
    asyncio.run(main())
