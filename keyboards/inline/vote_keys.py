from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import about_callback
feedscores = InlineKeyboardMarkup()
one_star = InlineKeyboardButton(text="🤮", callback_data=about_callback.new(feedback="1_star"))
two_stars = InlineKeyboardButton(text="😞", callback_data="name:2_stars")
three_stars = InlineKeyboardButton(text="😬", callback_data="name:3_stars")
four_stars = InlineKeyboardButton(text="☺️", callback_data="name:4_stars")
five_stars = InlineKeyboardButton(text="😍", callback_data="name:5_stars")
#cancel_vote = InlineKeyboardButton(text="Cancel", callback_data="name:cancel_vote")
#add_comment = InlineKeyboardButton(text="Add comment", callback_data="name:add_comment")

feedscores.row(one_star, two_stars, three_stars, four_stars, five_stars)


feedcomment = InlineKeyboardMarkup()
cancel_vote = InlineKeyboardButton(text="Cancel", callback_data="name:cancel_vote")
add_comment = InlineKeyboardButton(text="Add comment", callback_data="name:add_comment")
feedcomment.row(cancel_vote, add_comment)