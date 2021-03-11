from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_help(message: types.Message):
    text = ("Welcome home, master =^_^=")

    await message.answer(text)