from abc import update_abstractmethods
import os

import dotenv
import requests
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.functions.rights import is_Admin

from bot.handlers.logger import logger, print_msg
from bot.keyboards.default import (add_audio_list, add_favourite_audio_btn,
                                   add_menu, categories)
from bot.objects import data

dotenv.load_dotenv()


class Upload(StatesGroup):
    wait_name = State()
    wait_category = State()


@print_msg
async def start(message: types.Message, state: FSMContext):
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


async def send_audio(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, name = query.data.split("|")
    audio_file, audio_used = data.get_audio(category, name)
    await query.answer()
    await query.message.answer_chat_action('record_voice')
    await query.message.answer_audio(audio_file, 
                                    caption=f"Название: {name}\nИспользовано: {audio_used}",
                                    reply_markup=add_favourite_audio_btn(category, name, user_id))


async def add_favourites(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, name = query.data.split("|")
    user = data.get_user(user_id)
    if f"{category}|{name}" not in user['favourites']:
        user['favourites'].append(f"{category}|{name}")
    await query.message.edit_reply_markup(add_favourite_audio_btn(category, name, user_id))


async def remove_favourites(query: types.CallbackQuery):
    user_id = query.from_user.id
    action, category, name = query.data.split("|")
    user = data.get_user(user_id)
    if f"{category}|{name}" in user['favourites']:
        user['favourites'].remove(f"{category}|{name}")
    await query.message.edit_reply_markup(add_favourite_audio_btn(category, name, user_id))


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


async def ignore(query: types.CallbackQuery):
    await query.answer()


@is_Admin
async def new_audio(message: types.Message, state: FSMContext):
    file_info = await message.bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(os.getenv('TOKEN'), file_info.file_path))

    with open('src/temp.ogg','wb') as f:
        f.write(file.content)
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
    
    data.set_new_audio(category, name)
    await message.reply("Success!!!")
    await state.finish()



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

    dp.register_message_handler(new_audio, content_types=['voice'])
    dp.register_message_handler(audio_name, content_types=['text'], state=Upload.wait_name)

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
        ignore,
        lambda c: c.data == "ignore",
        state="*"
    )

    dp.register_callback_query_handler(
        delete_msg,
        lambda c: c.data == "delete",
        state="*"
    )
