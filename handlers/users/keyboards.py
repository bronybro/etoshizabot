import logging
import sqlite3

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data import quotes
from data.quotes import lst
from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.book_keys import pagination
# from data.quotes import quote, lst
from keyboards.inline.callback_datas import book_callback
from loader import dp
from states.round_state import Round


@dp.message_handler(Command("about"))
async def bot_about(message: Message):
    await message.answer(text="about this bot",
                         reply_markup=contact_buttons)


@dp.message_handler(Command("read"))
async def bot_read(message: Message):
    await message.answer(text=lst[0], reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page="prev"))
@dp.message_handler()
async def prev_page(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{call.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    if quote != 0:
        quote -= 1
    elif quote < 1:
        quote = len(lst) - 1
    logging.info(f" quote number={quote}|{lst[quote]}")
    quotes.cur.execute(f'UPDATE users SET user_page = "{quote}" WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page="next"))
async def next_page(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{call.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    if quote != len(lst) - 1:
        quote += 1
    elif quote >= len(lst) - 1:
        quote = 0
    logging.info(f" quote number={quote}|{lst[quote]}")
    quotes.cur.execute(f'UPDATE users SET user_page = "{quote}" WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)

