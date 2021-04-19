import typing

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from data import tables
from keyboards.inline.callback_datas import stock_callback, edit_callback
from keyboards.inline.edit_keys import edit_markup
from loader import dp, bot
from states.states import Stock, Edit


@dp.callback_query_handler(stock_callback.filter(action=['edit']), state=Stock.stock)
async def add_product(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.answer(cache_time=2)
    await call.message.answer(text='Send me number of product')
    await Edit.Q1.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=Edit.Q1)
async def is_digit_invalid(message: Message):
    await message.answer('Message text must be a number!')


@dp.message_handler(state=Edit.Q1)
async def choice_edit(message: Message, state: FSMContext):
    i = int(message.text) - 1
    tables.cur.execute(f'SELECT * FROM products')
    list = tables.cur.fetchall()
    try:
        text = '<b>#{id} {name}</b>\n{description}\n Price: <b>{price}</b>\n \n Choice what you want edit'.format(
            id=message.text,
            name=list[i][1],
            description=list[i][2],
            price=str(list[i][3])
        )
    except IndexError:
        await message.answer('No such product!')
    await state.update_data(id=list[i][0])
    await message.answer_photo(photo=list[i][4], caption=text, reply_markup=edit_markup)
    await Edit.next()


@dp.callback_query_handler(edit_callback.filter(
    edit=['name', 'description', 'price', 'photo','cancel']),
    state=Edit.Q2)
async def edit_item(call: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await call.answer(cache_time=2)
    callback_data_action = callback_data['edit']
    await state.update_data(action=callback_data_action)
    if callback_data_action == 'cancel':
        await Stock.stock.set()
        await call.message.answer(text='canceled')
    elif callback_data_action == 'photo':
        await Edit.Q3.set()
    else:
        await Edit.Q4.set()
    await call.message.answer(text=f'Send me new {callback_data_action}')


@dp.message_handler(state=Edit.Q3,content_types=types.ContentType.PHOTO)
async def edit_photo(message: Message, state: FSMContext):
    photo= message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    print(data["photo"])
    print( ' Ok')
    tables.cur.execute(f'UPDATE products SET photo="{data["photo"]}" WHERE item_id="{data["id"]}"')
    tables.conn.commit()
    await message.answer('Success!')


@dp.message_handler(state=Edit.Q4)
async def edit_text(message: Message, state: FSMContext):
    data = await state.get_data()
    if data['action'] == 'name':
        tables.cur.execute(f'UPDATE products SET product_name="{message.text}" WHERE item_id="{data["id"]}"')
    elif data['action'] == 'description':
        tables.cur.execute(f'UPDATE products SET product_description="{message.text}" WHERE item_id="{data["id"]}"')
    elif data['action'] == 'price':
        if message.text.isdigit():
            tables.cur.execute(f'UPDATE products SET price="{message.text}" WHERE item_id="{data["id"]}"')
            await message.answer('Success!')
        else:
            await message.reply('Must be an integer') #todo проверка на integer вынести отдельно
    tables.conn.commit()
    await message.answer('Success!')


