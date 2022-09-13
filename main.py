import asyncio
import os

from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv

from bot.handlers.default import register_handlers_default
from bot.handlers.secondary import register_handlers_secondary
from bot.handlers.logger import logger

dotenv.load_dotenv()


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/stop", description="Остановить"),
        BotCommand(command="/msg_to_admin", description="Написать сообщение админу"),
        BotCommand(command="/get_logfile", description="Получить Logs (admin)"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.info("Configuring...")
    
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_default(dp)
    register_handlers_secondary(dp)

    await set_commands(bot)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
