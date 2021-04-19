from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import edit_callback

edit_markup = InlineKeyboardMarkup()
edit_name = InlineKeyboardButton(text="name", callback_data=edit_callback.new(edit="name"))
edit_description = InlineKeyboardButton(text="description", callback_data="name:description")
edit_price = InlineKeyboardButton(text="price", callback_data="name:price")
edit_photo = InlineKeyboardButton(text="photo", callback_data="name:photo")
edit_cancel= InlineKeyboardButton(text="cancel", callback_data="name:cancel")
edit_markup.row(edit_name, edit_description)
edit_markup.row(edit_price, edit_photo)
edit_markup.row(edit_cancel)