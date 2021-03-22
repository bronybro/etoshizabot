import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data import quotes
from keyboards.default.languages import lang
from loader import dp


@dp.message_handler(CommandStart())
async def bot_help(message: types.Message):
    text = f"Welcome, {message.from_user.first_name}!  Please, choise language to use"

    x = quotes.cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    print(x)
    try:
        quotes.cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "0")')
        quotes.conn.commit()
    except sqlite3.IntegrityError:
        await message.answer("Welcome back!")
    else:
        quotes.cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
        result = quotes.cur.fetchall()
        print(f'Succes!{result}')
        await message.answer(text, reply_markup=lang)

