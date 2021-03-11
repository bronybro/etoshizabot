from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from data import quotes
from keyboards.inline.callback_datas import book_callback

pagination = InlineKeyboardMarkup()
previous = InlineKeyboardButton(text="◀", callback_data=book_callback.new(page="prev"))
next_page = InlineKeyboardButton(text="▶", callback_data="name:next")
pagination.row(previous, next_page)
