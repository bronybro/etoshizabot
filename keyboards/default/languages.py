from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

lang = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
en_locale = KeyboardButton(text="English")
lang.insert(en_locale)
ru_locale = KeyboardButton(text="Russian")
lang.insert(ru_locale)