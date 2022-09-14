import json
import os

from aiogram import types

data = {}


def start():
    global data
    with open("bot/objects/data.json", 'r') as file:
        data = json.loads(file.read())


def close():
    global data
    with open("bot/objects/data.json", 'w') as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


def new_user(user_id):
    user_id = str(user_id)
    global data
    data['users'][user_id] = {
        "id": user_id,
        "status": 0,
        "category": "Юмор",
        "favourites": []
    }


def check_user(user_id):
    user_id = str(user_id)
    global data
    return user_id in data['users']


def get_user(user_id):
    user_id = str(user_id)
    global data
    if check_user(user_id):
        return data['users'][user_id]
    else:
        new_user(user_id)
        return data['users'][user_id]


def get_audio(category, name):
    global data
    voice_id = data['audio'][category][name]['voice_id']
    user = data['audio'][category][name]['used']
    data['audio'][category][name]['used'] += 1
    return voice_id, user
        

def set_new_audio(category, name, voice_id):
    global data
    data['audio'][category][name] = {
        "name": f"{name}",
        "voice_id": voice_id,
        "used": 0
    }

