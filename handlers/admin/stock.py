
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data import tables
from data.config import config_text
from loader import dp
# TODO set admin flag check
from states.states import Stock



@dp.message_handler(Command("stock"), state='*')
async def get_emoji_flag(message: types.Message):
    json = config_text()
    tables.cur.execute(f'SELECT * FROM products WHERE product_id = "{message.text}"')
    flag = tables.cur.fetchone()

    if flag[0] == 0:
        status='<b>disabled</b>\n'
    else:
        status='<b>activated</b>\n'
    text= f'Komoji mode:{status}'+"\n".join(json['stock'])
    await message.answer(text=text)
    await Stock.flag.set()


@dp.message_handler(state=Stock.flag)
async def edit_product(message: Message, state:Stock.flag):

    flag = tables.cur.fetchone()
    # TODO state


    if flag[0] == 0:
        tables.cur.execute(f'UPDATE users SET emoji_flag=TRUE WHERE user_id = "{message.from_user.id}"')
        await message.answer(text='You have <b>activated</b> the emoji mode!')
    else:
        tables.cur.execute(f'UPDATE users SET emoji_flag=FALSE WHERE user_id = "{message.from_user.id}"')
        await message.answer(text='You have <b>disabled</b> the emoji mode!')

    tables.conn.commit()
    await state.finish()




