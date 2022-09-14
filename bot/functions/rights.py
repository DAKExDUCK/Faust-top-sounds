from functools import wraps

from aiogram import types

from bot.objects import data


admin_list = [626591599]


def is_Admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.from_user.id in admin_list:
            return await func(*args, **kwargs)
    return wrapper


def is_admin(user_id):
    return True if user_id in admin_list else False


def is_Sub(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        text = "💬 Для доступа к данной функции бота необходимо подписаться на каналы:\n\n"
        for channel in data.data['channels']:
            text += f"    [{channel['name']}]({channel['link']})\n"
        text += "\nКак только подписался, продолжи дальше пользоваться ботом"
        if args[0].__class__ is types.Message:
            message: types.Message = args[0]
            user_channel_status = await message.bot.get_chat_member(chat_id='-1001759691309', user_id=message.from_user.id)
            if user_channel_status["status"] == 'left' and not data.is_vip(message.from_user.id):
                await message.reply(text, parse_mode='MarkdownV2')
            else:
                return await func(*args, **kwargs)
        elif args[0].__class__ is types.CallbackQuery:
            query: types.CallbackQuery = args[0]
            user_channel_status = await query.bot.get_chat_member(chat_id='-1001759691309', user_id=query.from_user.id)
            if user_channel_status["status"] == 'left' and not data.is_vip(query.from_user.id):
                await query.message.answer(text, parse_mode='MarkdownV2')
            else:
                return await func(*args, **kwargs)
        
    return wrapper


async def is_sub(user_id, bot):
    user_channel_status = await bot.get_chat_member(chat_id='-1001759691309', user_id=user_id)
    if user_channel_status["status"] == 'left' and not data.is_vip(user_id):
        return False
    else:
        return True
