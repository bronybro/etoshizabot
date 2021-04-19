import logging
import typing

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.tables import lst
from keyboards.inline.callback_datas import show_callback
from keyboards.inline.show_keys import pagination
from loader import dp
from states.states import Comment


@dp.message_handler(Command("show"),state='*')
async def bot_read(message: Message, state: FSMContext):
    await state.finish()
    quote = 0
    await Comment.pages.set()
    state = dp.get_current().current_state()
    await state.update_data(quote=quote)
    print(await state.get_data())
    await message.answer(text=lst[quote], reply_markup=pagination)


@dp.callback_query_handler(show_callback.filter(page=['next', 'prev']), state=Comment.pages)
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
    elif callback_data_action == 'prev':
        if quote != 0:
            quote -= 1
        elif quote < 1:
            quote = len(lst) - 1
    # else:
    #     try:
    #         await call.message.answer('OK!')
    #     except MessageNotModified:
    #         print("WTF?")
    await state.update_data(quote=quote)
    logging.info(f" quote number={quote}|{lst[quote]}")
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)




# # TODO buy dialog
@dp.callback_query_handler(show_callback.filter(page=['buy']), state=Comment.pages)
async def buy_page(call: CallbackQuery, callback_data: typing.Dict[str, str],state:FSMContext):
    await state.finish()
    await call.answer(cache_time=2)
    await call.message.answer(text='OK!')
