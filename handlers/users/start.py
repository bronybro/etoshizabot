import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data import tables
from keyboards.default.languages import lang
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_help(message: types.Message):
    text = f"Welcome, {message.from_user.first_name}!  Please, choise language to use"

    try:
        tables.cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}","0","")')
        tables.conn.commit()
    except sqlite3.IntegrityError:
        await message.answer("Welcome back!")
    else:
        await message.answer(text, reply_markup=lang)

