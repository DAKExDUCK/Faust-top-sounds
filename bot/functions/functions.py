from aiogram import types


def clear_MD(text):
    text = str(text)
    symbols = ['_', '-', '*', '~', '[', ']', '(', ')', '`', '.']

    for sym in symbols:
        text = text.replace(sym, f"\{sym}")

    return text
