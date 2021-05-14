from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import DeleteMessage
from aiogram.types import CallbackQuery, Message
from data import tables
from handlers.admin import stock
from keyboards.inline.submit_keys import submit_cancel
from keyboards.inline.callback_datas import submit_callback, stock_callback
from loader import dp,bot
from states.states import Stock


@dp.callback_query_handler(stock_callback.filter(action=['add']), state=Stock.stock)
async def add_product(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.answer(text='Send me the product name')
    await Stock.next()


@dp.message_handler(state=Stock.Q1)
async def product_name(message: Message):
    state = dp.get_current().current_state()
    await state.update_data(name=message.text)
    await message.delete()
    #message = message.message_id-1
    await message.answer(text='Send me the product description')
    await Stock.next()


@dp.message_handler(state=Stock.Q2)
async def product_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text='Send me the product price')
    await Stock.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=Stock.Q3)
async def is_digit_invalid(message: Message):
    return await message.reply('Error! The price must be a number. For example 100')


@dp.message_handler(lambda message: message.text.isdigit(), state=Stock.Q3)
async def product_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer(text='Send me the photo of product')
    await Stock.next()


@dp.message_handler(state=Stock.Q4, content_types=types.ContentType.PHOTO)
async def product_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    tables.cur.execute(f'SELECT * FROM products')
    list = tables.cur.fetchall()
    text = '<b>#{id} {name}</b>\n{description}\n Price: <b>{price}</b>'.format( # FIXMI DRY next func()
        id=len(list) + 1,
        name=data['name'],
        description=data["description"],
        price=data['price']
    )
    await message.answer_photo(photo=data['photo'], caption=text, reply_markup=submit_cancel)
    await Stock.next()


@dp.callback_query_handler(submit_callback.filter(decision=['submit']), state=Stock.Q5)
async def submit_product(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    data = await state.get_data()
    tables.cur.execute(f'SELECT * FROM products')
    list = tables.cur.fetchall()
    try:
        last = max(list)
        print('test ', last[0])
        item_id = last[0] + 1
    except ValueError:
        item_id = 1

    print('max=', item_id)
    tables.cur.execute(
        f'INSERT INTO products VALUES({item_id},(?),(?),"{data["price"]}","{data["photo"]}")',
        (data["name"], data["description"],))
    tables.conn.commit()
    await state.reset_state()
    await call.message.delete()
    text = '<b>#{id} {name}</b>\n{description}\n Price: <b>{price}</b>'.format(
        id=len(list) + 1,
        name=data['name'],
        description=data["description"],
        price=data['price']
    )
    # TODO добаввить выбор постить или нет в бд сохранять ссылки на посты
    await bot.send_message(chat_id='@etoshizashop', text=text) 
    await stock.get_list(call.message)         


@dp.callback_query_handler(submit_callback.filter(decision=['cancel']), state=Stock.Q5)
async def reset_product(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.reset_state()
    await call.message.delete()
    await stock.get_list(call.message)
