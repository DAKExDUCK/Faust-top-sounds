import logging
from functools import wraps

from aiogram import types


logging.basicConfig(filename="logs.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt='%d/%m %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger()


def print_msg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message: types.Message = args[0]
        if message.chat.id == message.from_user.id:
            logger.info(f"{message.from_user.id} - {message.text}")
        else:
            logger.info(
                f"{message.from_user.id} / {message.chat.id} - {message.text}")
        return func(*args, **kwargs)
    return wrapper
