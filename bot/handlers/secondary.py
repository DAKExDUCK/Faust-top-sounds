import json

from aiogram import Dispatcher, types

from bot.functions.rights import is_Admin
from bot.handlers.logger import logger
from bot.keyboards.default import add_audio_list, add_favourites_audio_list
from bot.objects import data


async def audio_back(query: types.CallbackQuery):
    await query.answer()
    page = int(query.data.split("|")[1])
    if page == 0:
        return
    user_id = query.from_user.id
    user = data.get_user(user_id)
    audio_dict = data.data['audio'][user['category']]
    await query.message.edit_reply_markup(add_audio_list(user['category'], audio_dict, page))


async def audio_next(query: types.CallbackQuery):
    await query.answer()
    page = int(query.data.split("|")[1])
    if page == 0:
        return
    user_id = query.from_user.id
    user = data.get_user(user_id)
    audio_dict = data.data['audio'][user['category']]
    await query.message.edit_reply_markup(add_audio_list(user['category'], audio_dict, page))


async def audio_favourites_back(query: types.CallbackQuery):
    await query.answer()
    page = int(query.data.split("|")[1])
    if page == 0:
        return
    user_id = query.from_user.id
    user = data.get_user(user_id)
    await query.message.edit_reply_markup(add_favourites_audio_list(user, page))


async def audio_favourites_next(query: types.CallbackQuery):
    await query.answer()
    page = int(query.data.split("|")[1])
    if page == 0:
        return
    user_id = query.from_user.id
    user = data.get_user(user_id)
    await query.message.edit_reply_markup(add_favourites_audio_list(user, page))


async def ignore(query: types.CallbackQuery):
    await query.answer()


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


async def accept_join(request: types.ChatJoinRequest):
    await request.approve()


def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")
    dp.register_errors_handler(all_errors)

    dp.register_chat_join_request_handler(accept_join)
    
    dp.register_callback_query_handler(
        audio_back,
        lambda c: c.data.split("|")[0] == "audio_back",
        state="*"
    )
    dp.register_callback_query_handler(
        audio_next,
        lambda c: c.data.split("|")[0] == "audio_next",
        state="*"
    )
    dp.register_callback_query_handler(
        audio_favourites_back,
        lambda c: c.data.split("|")[0] == "audio_favourites_back",
        state="*"
    )
    dp.register_callback_query_handler(
        audio_favourites_next,
        lambda c: c.data.split("|")[0] == "audio_favourites_next",
        state="*"
    )
    dp.register_callback_query_handler(
        ignore,
        lambda c: c.data == "ignore",
        state="*"
    )
