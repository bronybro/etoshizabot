import logging
import typing
from loader import dp
from aiogram.dispatcher import FSMContext
from states.states import Comment
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.tables import lst
from keyboards.inline.book_keys import pagination
from keyboards.inline.callback_datas import book_callback


@dp.message_handler(Command("read"), state='*')
async def bot_read(message: Message, state: FSMContext):
    await state.finish()
    quote = 0
    await Comment.cs.set()
    state = dp.get_current().current_state()
    await state.update_data(quote=quote)
    print(await state.get_data())
    await message.answer(text=lst[quote], reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page=['next', 'prev']), state=Comment.cs)
async def prev_page(call: CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await call.answer(cache_time=2)
    callback_data_action = callback_data['page']
    x = await state.get_data()
    quote = x['quote']
    if callback_data_action == 'next':
        if quote != len(lst) - 1:
            quote += 1
        elif quote >= len(lst) - 1:
            quote = 0
    else:
        if quote != 0:
            quote -= 1
        elif quote < 1:
            quote = len(lst) - 1
    await state.update_data(quote=quote)
    logging.info(f" quote number={quote}|{lst[quote]}")
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)
