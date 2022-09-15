import json

from aiogram import Dispatcher, types

from bot.functions.rights import is_Admin
from bot.handlers.logger import logger
from bot.keyboards.default import add_audio_list, add_favourites_audio_list, show_categories, vip_status_btns
from bot.objects import data


async def vip_status(query: types.CallbackQuery):
    text = "🤩 Для получения VIP статуса оформите подписки по кнопки ниже.\n\n" \
            "Что дает подписка?\n" \
            "Полностью отключит всю рекламу и подписки на каналы + дает доступ " \
            "к оригинальничаем аудио стикерам. Тем самым вы поддерживаете развитие " \
            "нашего бота. а еще получаете лайк от админа ﻿😜﻿\n" \
            "Для того, чтобы оформить подписку, нажмите на кнопку ниже"
    await query.message.edit_text(text, reply_markup=vip_status_btns())


async def vip_status_free(query: types.CallbackQuery):
    user = data.get_user(query.from_user.id)
    text = "😎 Получите бонус от нашего бота\n\n" \
            "Вы можете получить VIP статус на неделю, пригласив 3 друзей по своей ссылке:\n" \
            f"https://t.me/{(await query.bot.get_me())['username']}?start=bonus-{user['id']}\n\n" \
            f"Всего приглашений: {user['friends']}\n\n" \
            "Отправь ссылку своим друзьям и за каждых 3-х друзей ты получишь VIP статус на неделю" \
            "P.s. подписки продляются"
    await query.message.edit_text(text, reply_markup=None)


async def change_category(query: types.CallbackQuery):
    await query.message.edit_text(
        "😎﻿Выберите какая категория вам больше нравится:\n\n"
        "При смене категории изменится список стикеров после кнопки 'Посмотреть список 🔍' ",
        reply_markup=show_categories()
)


async def chosen_change_category(query: types.CallbackQuery):
    action, category = query.data.split("|")
    user = data.get_user(query.from_user.id)
    user['category'] = category
    await query.answer(f"Режим изменён на {category}")


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
    logger.error(str(chat_id) + ' ' + str(text) + ' ' + str(error), exc_info=True)


async def accept_join(request: types.ChatJoinRequest):
    await request.approve()


def register_handlers_secondary(dp: Dispatcher):
    dp.register_message_handler(send_log, commands="get_logfile", state="*")
    dp.register_errors_handler(all_errors)

    dp.register_chat_join_request_handler(accept_join)

    dp.register_callback_query_handler(
        vip_status,
        lambda c: c.data == "vip_status",
        state="*"
    )
    dp.register_callback_query_handler(
        vip_status_free,
        lambda c: c.data == "vip_status|free",
        state="*"
    )

    dp.register_callback_query_handler(
        change_category,
        lambda c: c.data == "change_category",
        state="*"
    )
    dp.register_callback_query_handler(
        chosen_change_category,
        lambda c: c.data.split("|")[0] == "change_category",
        state="*"
    )
    
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
