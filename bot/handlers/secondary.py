from datetime import datetime, timedelta

from aiogram import Dispatcher, types
from bot.functions.functions import get_info_from_forwarded_msg
from bot.functions.rights import is_Admin, is_admin
from bot.handlers.logger import logger
from bot.keyboards.default import add_delete_button
from bot.objects.chats import chat_store


@is_Admin
async def send_log(message: types.Message):
    with open('logs.log', 'r') as logs:
        await message.reply_document(logs)


async def last_handler(message: types.Message):
    if is_admin(message.from_user.id) and message.is_forward():
        text, user_id, name, mention = get_info_from_forwarded_msg(message)
        if len(text) > 0:
            await message.reply(text, parse_mode='MarkdownV2', reply_markup=add_delete_button())
    else:
        if (message.chat.id in chat_store or message.reply_to_message.forward_from.id in chat_store) and message.reply_to_message:
            if message.reply_to_message.is_forward():
                chat_data = chat_store[message.reply_to_message.forward_from.id]
                chat_id = chat_data['user']
                from_id = chat_data['admin']
            else:
                chat_data = chat_store[message.chat.id]
                chat_id = chat_data['admin']
                from_id = chat_data['user']

            if datetime.now() - chat_data['date'] > timedelta(seconds=1):
                chat_data['date'] = datetime.now()
                await message.bot.send_message(chat_id, f"Message from `{from_id}`:", parse_mode='MarkdownV2')
            await message.forward(chat_id)


def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")

    dp.register_message_handler(last_handler, content_types=['text', 'document', 'photo'], state="*")
