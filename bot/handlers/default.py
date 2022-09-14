import dotenv
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.functions.rights import is_Admin, is_Sub, is_sub
from bot.handlers.logger import logger, print_msg
from bot.keyboards.default import (add_audio_list, add_favourite_audio_btn,
                                   add_favourites_audio_list, add_menu,
                                   categories, profile_menu)
from bot.objects import data

dotenv.load_dotenv()


class Upload(StatesGroup):
    wait_name = State()
    wait_category = State()


@print_msg
async def start(message: types.Message, state: FSMContext):
    if len(message.get_args()):
        args = message.get_args()
        action = args.split("-")[0]
        if action == "bonus":
            id = args.split("-")[1]
            if not data.check_user(message.from_user.id):
                data.new_user(message.from_user.id)
                user = data.get_user(id)
                user['friends'] += 1
                if user['friends'] % 3 == 0:
                    data.set_vip(user['id'])
                    try:
                        await message.bot.send_message("Вам был выдан VIP статус на неделю")
                    except:
                        ...
        elif action == "unlock":
            text = "💬 Для доступа к данной функции бота необходимо подписаться на каналы:\n\n"
            for channel in data.data['channels']:
                text += f"    [{channel['name']}]({channel['link']})\n"
            text += "\nКак только подписался, продолжи дальше пользоваться ботом"
            await message.answer(text, parse_mode='MarkdownV2')
            return


    text = "Привет ✌️!\n" \
        "Я-бот который поможет тебе  оригинально ответить на сообщение друга!\n\n" \
        "Также я работаю в inline-режиме\n\n" \
        "Для начала нажми на кнопку: 'Посмотреть список🔍'"
    await message.reply(text, reply_markup=add_menu())
    await state.finish()


@print_msg
async def show_list(message: types.Message, state: FSMContext):
    user = data.get_user(message.from_user.id)
    audio_dict = data.data['audio'][user['category']]
    await message.reply(f"Категория: {user['category']}", reply_markup=add_audio_list(user['category'], audio_dict, 1))


@is_Sub
@print_msg
async def show_list_favourites(message: types.Message, state: FSMContext):
    user = data.get_user(message.from_user.id)
    await message.reply(f"Категория: Избранные", reply_markup=add_favourites_audio_list(user, 1))


@print_msg
async def profile(message: types.Message, state: FSMContext):
    user = data.get_user(message.from_user.id)
    text = "👤 Ваш профиль\n" \
            "➖➖➖➖➖➖➖\n" \
            f"👥Друзей: {user['friends']}\n" \
            f"😎VIP Статус: {'да' if data.is_vip(user['id']) else 'нет'}\n" \
            "➖➖➖➖➖➖➖\n" \
            f"🗯Добавил в избранное: {len(user['favourites'])}\n" \
            "➖➖➖➖➖➖➖\n" \
            f"♻️Режим: {user['category']}"
    await message.reply(text, reply_markup=profile_menu())


@is_Sub
async def send_audio(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, index = query.data.split("|")
    name, voice_id, audio_used = data.get_audio(category, index)
    await query.answer()
    await query.message.answer_chat_action('record_voice')
    await query.message.answer_audio(voice_id, 
                                    caption=f"Название: {name}\nИспользовано: {audio_used}",
                                    reply_markup=add_favourite_audio_btn(category, index, user_id, name))


@is_Sub
async def add_favourites(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, index = query.data.split("|")
    name, voice_id, audio_used = data.get_audio(category, index)
    user = data.get_user(user_id)
    if f"{category}|{index}" not in user['favourites']:
        user['favourites'].append(f"{category}|{index}")
    await query.message.edit_reply_markup(add_favourite_audio_btn(category, index, user_id, name))


async def remove_favourites(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, index = query.data.split("|")
    name, voice_id, audio_used = data.get_audio(category, index)
    user = data.get_user(user_id)
    if f"{category}|{index}" in user['favourites']:
        user['favourites'].remove(f"{category}|{index}")
    await query.message.edit_reply_markup(add_favourite_audio_btn(category, index, user_id, name))


@is_Admin
async def new_category(message: types.Message):
    arg = message.get_args()
    if len(arg) == 0:
        await message.reply("Usage: /new_cat Юмор")
    else:
        list = [a.lower() for a in data.data['audio']]
        if arg.lower() not in list:
            data.data['audio'][arg] = {}
            await message.answer(f"{arg} category created!")
        else:
            await message.answer(f"This category is already in data")


@is_Admin
async def new_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as d:
        d['voice_id'] = message.voice.file_id
    await Upload.wait_category.set()

    await message.reply("Audio uploaded, choose category", reply_markup=categories())


async def set_audio_category(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as d:
        d['category'] = query.data.split("|")[1]
    await Upload.wait_name.set()
    await query.message.answer("Now write name for new audio:")


async def audio_name(message: types.Message, state: FSMContext):
    name = message.text
    async with state.proxy() as d:
        category = d['category']
        voice_id = d['voice_id']
    
    data.set_new_audio(category, name, voice_id)
    await message.reply("Success!!!")
    await state.finish()


async def show_audio_list(inline_query: types.InlineQuery):
    if not await is_sub(inline_query.from_user.id, inline_query.bot):
        results = [
            types.InlineQueryResultArticle(
                        id=0,
                        title="Заблокировано",
                        description="Чтобы разблокировать, перейдите к боту",
                        input_message_content=types.InputTextMessageContent(
                            message_text="t.me/" + (await inline_query.bot.get_me())['username'] + "?start=unlock"
                        )
            )
        ]
        await inline_query.answer(results, is_personal=True, cache_time=None)
        return
    results = []
    index = 0
    if len(inline_query.query) == 0:
        for category in data.data['audio']:
            category = data.data['audio'][category]
            for audio in category:
                audio = category[audio]
                results.append(
                    types.InlineQueryResultVoice(
                        id=index,
                        voice_url=audio['voice_id'],
                        title=audio['name']
                        )
                )
                index += 1
    else:
        for category in data.data['audio']:
            category = data.data['audio'][category]
            for audio in category:
                audio = category[audio]
                if inline_query.query.lower() in audio['name'].lower():
                    results.append(
                        types.InlineQueryResultVoice(
                            id=index,
                            voice_url=audio['voice_id'],
                            title=audio['name']
                            )
                    )
                    index += 1
    await inline_query.answer(results, is_personal=True, cache_time=None)


async def delete_msg(query: types.CallbackQuery):
    try:
        await query.bot.delete_message(query.message.chat.id, query.message.message_id)
        if query.message.reply_to_message:
            await query.bot.delete_message(query.message.chat.id, query.message.reply_to_message.message_id)
        await query.answer()
    except Exception as exc:
        logger.error(exc)
        await query.answer("Error")
  

def register_handlers_default(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(help, commands="help", state="*")
    dp.register_message_handler(show_list, lambda msg: msg.text == "Посмотреть список🔍", content_types=['text'])
    dp.register_message_handler(show_list_favourites, lambda msg: msg.text == "🔔Избранное", content_types=['text'])
    dp.register_message_handler(profile, lambda msg: msg.text == "👮‍♀Профиль", content_types=['text'])

    dp.register_message_handler(new_category, commands="new_cat", state="*")

    dp.register_message_handler(new_audio, content_types=['voice'])
    dp.register_message_handler(audio_name, content_types=['text'], state=Upload.wait_name)

    dp.register_inline_handler(show_audio_list)

    dp.register_callback_query_handler(
        set_audio_category,
        lambda c: c.data.split("|")[0] == "set_audio_category",
        state="*"
    )

    dp.register_callback_query_handler(
        send_audio,
        lambda c: c.data.split("|")[0] == "audio",
        state="*"
    )
    dp.register_callback_query_handler(
        add_favourites,
        lambda c: c.data.split("|")[0] == "add_favourites",
        state="*"
    )
    dp.register_callback_query_handler(
        remove_favourites,
        lambda c: c.data.split("|")[0] == "remove_favourites",
        state="*"
    )

    dp.register_callback_query_handler(
        delete_msg,
        lambda c: c.data == "delete",
        state="*"
    )
