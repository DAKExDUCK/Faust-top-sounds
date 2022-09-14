import json
from datetime import datetime

from dateutil.relativedelta import relativedelta

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
        "friends": 0,
        "end_date": None,
        "favourites": []
    }


def set_vip(user_id):
    if not check_user(user_id):
        new_user(user_id)
    user = get_user(user_id)
    if user['end_date'] is None:
        user['end_date'] = str(datetime.now() + relativedelta(weeks=1))
    elif datetime.strptime(user['end_date'], '%Y-%m-%d %H:%M:%S.%f') > datetime.now():
        user['end_date'] = str(datetime.strptime(user['end_date'], '%Y-%m-%d %H:%M:%S.%f') + relativedelta(weeks=1))
    elif datetime.strptime(user['end_date'], '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
        user['end_date'] = str(datetime.now() + relativedelta(weeks=1))


def is_vip(user_id):
    if check_user(user_id):
        user = get_user(user_id)
        date_str = user['end_date']
        if date_str is None:
            return False

        if datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f') > datetime.now():
            return True
        else:
            return False
    else:
        return False


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


def get_audio(category, index):
    global data
    voice_id = data['audio'][category][index]['voice_id']
    name = data['audio'][category][index]['name']
    user = data['audio'][category][index]['used']
    data['audio'][category][index]['used'] += 1
    return name, voice_id, user
        

def set_new_audio(category, name, voice_id):
    global data
    index = int(sorted(data['audio'][category].keys())[-1]) + 1
    data['audio'][category][index] = {
        "name": f"{name}",
        "voice_id": voice_id,
        "used": 0
    }

