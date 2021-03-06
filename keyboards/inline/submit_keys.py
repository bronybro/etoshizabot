from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import submit_callback

submit_cancel = InlineKeyboardMarkup()
submit = InlineKeyboardButton(text="✅", callback_data=submit_callback.new(decision="submit"))
cancel = InlineKeyboardButton(text="❌", callback_data="name:cancel")
submit_cancel.row(submit, cancel)