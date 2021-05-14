import sqlite3
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.types import Chat
from loader import dp, bot
from states.states import Channel
from data import config, tables

@dp.message_handler(Command('addch'), state='*')
async def await_channel(message:Message):
    await message.answer('Send me channelid:')
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        )
    await Channel.Q1.set()

@dp.message_handler(state=Channel.Q1)
async def add_channel(message:Message, state: FSMContext):

    text = f"The channel is connected"

    try:  # TODO проверка на то существует ли такой канал в телеграм
        tables.cur.execute(f'INSERT INTO channels VALUES("{message.text}")')
        tables.conn.commit()
    except sqlite3.IntegrityError:
        await message.answer(f"The channel {message.text} is already connected!")
    else:
        await message.answer(f"The channel {message.text} is connected!")


