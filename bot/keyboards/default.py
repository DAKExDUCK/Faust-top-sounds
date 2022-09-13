import math
from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup, InlineKeyboardButton)


from bot.objects import data


def add_delete_button(kb: types.inline_keyboard = None):
    if kb is None:
        kb = InlineKeyboardMarkup()
    del_btn = InlineKeyboardButton('Delete', callback_data=f'delete')
    kb.add(del_btn)

    return kb


def add_menu():
    show_list = KeyboardButton('Посмотреть список🔍')
    favourites = KeyboardButton('🔔Избранное')
    profile = KeyboardButton('👮‍♀Профиль')

    menu = ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add(show_list)
    menu.row(favourites, profile)

    return menu


def add_audio_list(category, audio_dict, page):
    kb = InlineKeyboardMarkup()

    list = []
    for audio_key in audio_dict:
        list.append(audio_key)

    min = 0 + ((page-1)*10)
    max = page*10

    if page != 1:
        page_back = page-1
    else:
        page_back = 0
    if page != math.ceil(len(audio_dict)/10):
        page_next = page+1
    else:
        page_next = 0

    for audio in list[min:max]:
        kb.add(InlineKeyboardButton(audio, callback_data=f"audio|{category}|{audio}"))

    kb.row(
        InlineKeyboardButton("<", callback_data=f"audio_back|{page_back}"),
        InlineKeyboardButton(f"{page}/{math.ceil(len(audio_dict)/10)}", callback_data=f"ignore"),
        InlineKeyboardButton(">", callback_data=f"audio_next|{page_next}")
    )
    return kb


def add_favourite_audio_btn(category, name, user_id):
    kb = InlineKeyboardMarkup()
    audio_name = f"{category}|{name}"

    if audio_name in data.get_user(user_id)['favourites']:
        kb.add(InlineKeyboardButton('Убрать их Избранных', callback_data=f"remove_favourites|{audio_name}"))
    else:
        kb.add(InlineKeyboardButton('Добавить в Избранное', callback_data=f"add_favourites|{audio_name}"))

    return kb


def categories():
    kb = InlineKeyboardMarkup()
    for category in data.data['audio']:
        kb.add(InlineKeyboardButton(category, callback_data=f"set_audio_category|{category}"))

    return kb