from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import about_callback

contact_buttons = InlineKeyboardMarkup(row_width=2)
tg = InlineKeyboardButton(text="Telegram", callback_data=about_callback.new(social="tg"))
contact_buttons.add(tg)
twi = InlineKeyboardButton(text="Twitter", callback_data="name:twi")
contact_buttons.add(twi)
