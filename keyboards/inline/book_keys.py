from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import book_callback

pagination = InlineKeyboardMarkup(row_width=3, )
previous = InlineKeyboardButton(text="-", callback_data=book_callback.new(page="prev"))
page = InlineKeyboardButton(text="1", callback_data="page:page")
next_page = InlineKeyboardButton(text="+", callback_data="page:next")
pagination.row(previous, page, next_page)
