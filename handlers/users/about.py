import typing

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data import tables
from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.callback_datas import about_callback
from keyboards.inline.vote_keys import feedscores, feedcomment
from loader import dp
from states.states import Comment


@dp.message_handler(Command("about"),state='*')
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
        await Comment.vote.set()
        await call.message.edit_text(text="Type you comment..",
                                     reply_markup='')
    else:
        x = callback_data_action[0]
        tables.cur.execute(f'UPDATE users SET user_vote = {x} WHERE user_id = "{call.from_user.id}"')
        tables.conn.commit()
        await call.message.edit_text(text=f"{x}/5",
                                     reply_markup=feedcomment)


@dp.message_handler(state=Comment.vote)
async def waiting_vote(message: Message, state: FSMContext):
    print(message.text)
    tables.cur.execute(f'UPDATE users SET user_comment = "{message.text}" WHERE user_id = "{message.from_user.id}"')
    tables.conn.commit()
    await state.finish()
    await message.answer(text='Thank yor for vote and review!')
