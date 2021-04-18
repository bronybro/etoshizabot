from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from data.config import config_text
from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    json = config_text()
    text = json['help']
    await message.answer("\n".join(text))