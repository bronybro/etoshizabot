from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from data import tables
from handlers.admin import stock, edit
from keyboards.inline.callback_datas import stock_callback
from loader import dp
from states.states import Stock, Delete


@dp.callback_query_handler(stock_callback.filter(action=['delete']), state=Stock.stock)
async def choice_item(call: CallbackQuery, state: FSMContext):
    await edit.edit_product(call, state)
    await Delete.Q1.set()


@dp.message_handler(state=Delete.Q1)
async def delete_item(message: Message, state: FSMContext):
    tables.cur.execute(f'DELETE FROM products WHERE ROWID="{message.text}"')
    tables.conn.commit()
    #await state.finish()
    await stock.get_list(message)
