from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import stock_callback

stock = InlineKeyboardMarkup()
add = InlineKeyboardButton(text="add", callback_data=stock_callback.new(action="add"))
edit = InlineKeyboardButton(text="edit", callback_data="name:edit")
delete = InlineKeyboardButton(text="delete", callback_data="name:delete")
stock.row(add, edit, delete)