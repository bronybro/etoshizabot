import logging
import typing

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data import quotes
from data.quotes import lst
from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.book_keys import pagination
from keyboards.inline.callback_datas import book_callback, about_callback
from keyboards.inline.vote_keys import feedscores, feedcomment
from loader import dp
from states.round_state import Comment


@dp.message_handler(Command("about"))
async def bot_about(message: Message):
    await message.answer(text=f'about this bot\nThis bot use <b>aiogram</b>\
\n You <code>user_id="{message.from_user.id}"</code>',
                         reply_markup=contact_buttons)


@dp.callback_query_handler(about_callback.filter(
    feedback=['feed', '1_star', '2_stars', '3_stars', '4_stars', '5_stars', 'cancel_vote', 'add_comment']))
async def vote(call: CallbackQuery, callback_data: typing.Dict[str, str]):
    await call.answer(cache_time=2)
    callback_data_action = callback_data['feedback']
    if callback_data_action == 'feed':
        await call.message.edit_text(text="Are you like this bot?",
                                     reply_markup=feedscores)
    elif callback_data_action == 'cancel_vote':
        await call.message.edit_text(text="Thank you for vote!",
                                     reply_markup='')
    elif callback_data_action == 'add_comment':
        await Comment.cs.set()
        await call.message.edit_text(text="Type you comment..",
                                     reply_markup='')
    else:
        x = callback_data_action[0]
        print(x)
        quotes.cur.execute(f'UPDATE users SET user_vote = {x} WHERE user_id = "{call.from_user.id}"')
        quotes.conn.commit()
        await call.message.edit_text(text="1/5",
                                     reply_markup=feedcomment)


'''сохраняем комментарий и выходим из состояния'''


@dp.message_handler(state=Comment.cs)
async def waiting_review(message: Message, state: FSMContext):
    print(message.text)
    quotes.cur.execute(f'UPDATE users SET user_comment = "{message.text}" WHERE user_id = "{message.from_user.id}"')
    quotes.conn.commit()
    await state.finish()
    await message.answer(text='Thank yor for vote and review!')


# TODO вынести в отдельный модуль
@dp.message_handler(Command("read"))
async def bot_read(message: Message):
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{message.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    await message.answer(text=lst[quote], reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page=['next', 'prev']))
async def prev_page(call: CallbackQuery, callback_data: typing.Dict[str, str]):
    await call.answer(cache_time=2)
    callback_data_action = callback_data['page']
    print(callback_data_action)
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{call.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]  # FIXME переписать как константу и хранить в FSM

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
    # TODO Наполнять lst динамически
    logging.info(f" quote number={quote}|{lst[quote]}")
    quotes.cur.execute(f'UPDATE users SET user_page = "{quote}" WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)
