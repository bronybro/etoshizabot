from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import URL_TELEGRAM, URL_TWITTER
#  from keyboards.inline.callback_datas import about_callback

contact_buttons = InlineKeyboardMarkup(row_width=2)
tg = InlineKeyboardButton(text="Telegram", url=URL_TELEGRAM)
contact_buttons.insert(tg)
twi = InlineKeyboardButton(text="Twitter", url=URL_TWITTER)
contact_buttons.insert(twi)
