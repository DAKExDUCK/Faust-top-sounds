import math

from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
                           
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
        kb.add(InlineKeyboardButton(audio_dict[audio]['name'], callback_data=f"audio|{category}|{audio}"))

    kb.row(
        InlineKeyboardButton("<", callback_data=f"audio_back|{page_back}"),
        InlineKeyboardButton(f"{page}/{math.ceil(len(audio_dict)/10)}", callback_data=f"ignore"),
        InlineKeyboardButton(">", callback_data=f"audio_next|{page_next}")
    )
    return kb


def add_favourites_audio_list(user, page):
    kb = InlineKeyboardMarkup()

    min = 0 + ((page-1)*10)
    max = page*10

    if page != 1:
        page_back = page-1
    else:
        page_back = 0
    if page != math.ceil(len(user['favourites'])/10):
        page_next = page+1
    else:
        page_next = 0

    for index in range(min, max):
        if index>=len(user['favourites']):
            break
        category = user['favourites'][index].split("|")[0]
        i = user['favourites'][index].split("|")[1]
        name, voice_id, audio_used = data.get_audio(category, i)

        kb.add(InlineKeyboardButton(name, callback_data=f"audio|{user['favourites'][index]}"))

    kb.row(
        InlineKeyboardButton("<", callback_data=f"audio_favourites_back|{page_back}"),
        InlineKeyboardButton(f"{page}/{math.ceil(len(user['favourites'])/10)}", callback_data=f"ignore"),
        InlineKeyboardButton(">", callback_data=f"audio_favourites_next|{page_next}")
    )
    return kb


def add_favourite_audio_btn(category, index, user_id, name):
    kb = InlineKeyboardMarkup()
    audio = f"{category}|{index}"
    kb.add(InlineKeyboardButton('Отправить другу', switch_inline_query=name))
    if audio in data.get_user(user_id)['favourites']:
        kb.add(InlineKeyboardButton('Убрать их Избранных', callback_data=f"remove_favourites|{audio}"))
    else:
        kb.add(InlineKeyboardButton('Добавить в Избранное', callback_data=f"add_favourites|{audio}"))

    return kb


def categories():
    kb = InlineKeyboardMarkup()
    index = 1
    for category in data.data['audio']:
        if index%2!=1:
            kb.insert(InlineKeyboardButton(category, callback_data=f"set_audio_category|{category}"))
        else:
            kb.add(InlineKeyboardButton(category, callback_data=f"set_audio_category|{category}"))
        index+=1
    return kb


def profile_menu():
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("♻️Сменить Режим", callback_data=f"change_category"),
        InlineKeyboardButton("♻️VIP Статус", callback_data=f"vip_status")
        )

    return kb


def vip_status_btns():
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("Получить бесплатно", callback_data=f"vip_status|free"))
    kb.add(InlineKeyboardButton("На месяц - 100руб", callback_data=f"vip_status|1"))
    kb.add(InlineKeyboardButton("На 3 месяца - 250руб", callback_data=f"vip_status|3"))
    kb.add(InlineKeyboardButton("На 6 месяцев - 450руб", callback_data=f"vip_status|6"))
    kb.add(InlineKeyboardButton("Навсегда - 999руб", callback_data=f"vip_status|forever"))


    return kb


def show_categories():
    kb = InlineKeyboardMarkup()

    index = 1
    for category in data.data['audio']:
        if index%2!=1:
            kb.insert(InlineKeyboardButton(category, callback_data=f"change_category|{category}"))
        else:
            kb.add(InlineKeyboardButton(category, callback_data=f"change_category|{category}"))
        index+=1

    return kb