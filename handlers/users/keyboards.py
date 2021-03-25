import logging
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode

from data import quotes
from data.quotes import lst
from keyboards.inline import vote_keys
from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.book_keys import pagination
# from data.quotes import quote, lst
from keyboards.inline.callback_datas import book_callback, about_callback
from keyboards.inline.vote_keys import feedscores, feedcomment
from loader import dp
from states.round_state import Comment


@dp.message_handler(Command("about"))
async def bot_about(message: Message):
    await message.answer(text=f'about this bot\nThis bot use <b>aiogram</b>\
\n You <code>user_id="{message.from_user.id}"</code>',
                         reply_markup=contact_buttons)


@dp.callback_query_handler(about_callback.filter(feedback="feed"))
async def add_score(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_text(text="Are you like this bot?",
                                 reply_markup=feedscores)


@dp.callback_query_handler(about_callback.filter(feedback="cancel_vote"))
async def add_score(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_text(text="Thank you for vote!",
                                 reply_markup='')


# тут будет функция ожидания ответа от пользователя
@dp.callback_query_handler(about_callback.filter(feedback="1_star"))
async def vote_1(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'UPDATE users SET user_vote = 1 WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text="1/5",
                                 reply_markup=feedcomment)


@dp.callback_query_handler(about_callback.filter(feedback="2_stars"))
async def vote_2(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'UPDATE users SET user_vote = 2 WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text="2/5",
                                 reply_markup=feedcomment)


@dp.callback_query_handler(about_callback.filter(feedback="3_stars"))
async def vote_3(call: CallbackQuery):
    await call.answer(cache_time=2)

    await call.message.edit_text(text=f'<b>You vote:</b>3/5',
                                 reply_markup=feedcomment)


@dp.callback_query_handler(about_callback.filter(feedback="4_stars"))
async def vote_4(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_text(text="4/5",
                                 reply_markup=feedcomment)


@dp.callback_query_handler(about_callback.filter(feedback="5_stars"))
async def vote_5(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.edit_text(text="5/5",
                                 reply_markup=feedcomment)


'''Устанавливаем состояние'''
@dp.callback_query_handler(about_callback.filter(feedback="add_comment"))
async def feed_comment(call: CallbackQuery):
    await Comment.cs.set()
    await call.message.edit_text(text="Type you comment..",
                                 reply_markup='')

'''сохраняем комментарий и выходим из состояния'''
@dp.message_handler(state=Comment.cs)
async def waiting_review(message: Message, state: FSMContext):
    print(message.text)
    quotes.cur.execute(f'UPDATE users SET user_comment = "{message.text}" WHERE user_id = "{message.from_user.id}"')
    quotes.conn.commit()
    await state.finish()
    await message.answer(text='Thank yor for vote and review!')


@dp.message_handler(Command("read"))
async def bot_read(message: Message):
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{message.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    #await Comment.cs.set()
    await message.answer(text=lst[quote], reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page="prev"))
# @dp.message_handler()
async def prev_page(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{call.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    if quote != 0:
        quote -= 1
    elif quote < 1:
        quote = len(lst) - 1
    logging.info(f" quote number={quote}|{lst[quote]}")
    quotes.cur.execute(f'UPDATE users SET user_page = "{quote}" WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)


@dp.callback_query_handler(book_callback.filter(page="next"))
async def next_page(call: CallbackQuery):
    await call.answer(cache_time=2)
    quotes.cur.execute(f'SELECT user_page FROM users WHERE user_id = "{call.from_user.id}"')
    x = list(quotes.cur.fetchone())
    quote = x[0]
    if quote != len(lst) - 1:
        quote += 1
    elif quote >= len(lst) - 1:
        quote = 0
    logging.info(f" quote number={quote}|{lst[quote]}")
    quotes.cur.execute(f'UPDATE users SET user_page = "{quote}" WHERE user_id = "{call.from_user.id}"')
    quotes.conn.commit()
    await call.message.edit_text(text=lst[quote],
                                 reply_markup=pagination)
