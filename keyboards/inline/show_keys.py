from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import show_callback

pagination = InlineKeyboardMarkup()
previous = InlineKeyboardButton(text="◀", callback_data=show_callback.new(page="prev"))
next_page = InlineKeyboardButton(text="▶", callback_data="name:next")
buy = InlineKeyboardButton(text="BUY", callback_data=show_callback.new(page="buy"))
pagination.row(previous, next_page)
pagination.row(buy)
