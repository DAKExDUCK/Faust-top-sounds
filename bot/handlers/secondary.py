from aiogram import Dispatcher, types
from bot.functions.rights import is_Admin


@is_Admin
async def send_log(message: types.Message):
    with open('logs.log', 'r') as logs:
        await message.reply_document(logs)


def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")

