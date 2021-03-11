import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import book_callback
from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.book_keys import pagination
from loader import dp


@dp.message_handler(Command("about"))
async def bot_about(message: Message):
    await message.answer(text="about this bot",
                         reply_markup=contact_buttons)


@dp.message_handler(Command("read"))
async def bot_about(message: Message):
    await message.answer(text="example",
                         reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page="prev"))
async def prev_page(call: CallbackQuery):
    await call.answer(cache_time=5)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("-")


@dp.callback_query_handler(book_callback.filter(page="next"))
async def next_page(call: CallbackQuery):
    await call.answer(cache_time=5)
    callback_data = call.data
    logging.info(f"call = {callback_data}")
    await call.message.answer("+")
