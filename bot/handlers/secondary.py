import json

from aiogram import Dispatcher, types

from bot.functions.rights import is_Admin
from bot.handlers.logger import logger


@is_Admin
async def send_log(message: types.Message):
    with open('logs.log', 'r') as logs:
        await message.reply_document(logs)


async def all_errors(update: types.Update, error):
    update_json = {}
    update_json = json.loads(update.as_json())
    if 'callback_query' in update_json.keys():
        await update.callback_query.answer('Error')
        chat_id = update.callback_query.from_user.id
        text = update.callback_query.data
    elif 'message' in update_json.keys():
        await update.message.answer('Error')
        chat_id = update.message.from_user.id
        text = update.message.text
    logger.error(str(chat_id) + str(text) + str(error), exc_info=True)
  

def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")
    dp.register_errors_handler(all_errors)
    
