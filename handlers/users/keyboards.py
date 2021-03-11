from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.inline.about_keys import contact_buttons
from keyboards.inline.book_keys import pagination
from loader import dp


@dp.message_handler(Command("about"))
async def bot_about(message: Message):
    await message.answer(text="Контакты создателя:",
                         reply_markup=contact_buttons)


@dp.message_handler(Command("read"))
async def bot_about(message: Message):
    # text = # сюда переменную с названием статьи
    await message.answer(text="Это пример простой читалки",
                         reply_markup=pagination)
