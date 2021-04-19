from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from data import tables
# from data.config import config_text
from keyboards.inline.stock_keys import stock
from loader import dp
# TODO set admin flag check
from states.states import Stock


@dp.message_handler(Command("stock"), state='*')
async def get_list(message: Message):
    # json = config_text()
    tables.cur.execute(f'SELECT * FROM products')
    list = tables.cur.fetchall()
    print(list)
    text=''
    # TODO exception for []
    for i in range(0, len(list)):
        text += '#{0}. {1} - {2}\n'.format(i+1,list[i][0], list[i][2])
    await Stock.stock.set()
    await message.answer(text=text, reply_markup=stock)
    #await Stock.stock.set()



