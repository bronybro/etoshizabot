from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from data import tables
from loader import dp

# TODO set admin flag check
@dp.message_handler(Command("emoji"), state='*')
async def set_emoji_flag(message: Message):
    tables.cur.execute(f'SELECT emoji_flag FROM users WHERE user_id = "{message.from_user.id}"')
    x = tables.cur.fetchone()
    # TODO state


    if x[0] == 0:
        tables.cur.execute(f'UPDATE users SET emoji_flag=TRUE WHERE user_id = "{message.from_user.id}"')
    else:
        tables.cur.execute(f'UPDATE users SET emoji_flag=FALSE WHERE user_id = "{message.from_user.id}"')

    tables.cur.execute(f'SELECT emoji_flag FROM users WHERE user_id = "{message.from_user.id}"')
    x = tables.cur.fetchone()
    tables.conn.commit()

    await message.answer(text='{0} komoji mode'.format(x[0]))


