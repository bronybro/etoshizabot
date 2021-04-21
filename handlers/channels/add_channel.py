from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
#from dotenv
from aiogram.types import Chat
import logging
from loader import dp
from states.states import Channel
from loader import bot
from data import config

@dp.message_handler(Command('addch'), state='*')
async def await_channel(message:Message):
    await message.answer('Send me channelid:')
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO,
                        )
    await Channel.Q1.set()

@dp.message_handler(state=Channel.Q1)
async def add_channel(message:Message, state: FSMContext):
    test = open(".env", "r")
    print(test.readlines())
    with open(".env", "a") as f:
        
        
        f.write(f"CHANNEL_ID={message.text}\n") # todo проверка на указан ли канал в config

    #TODO 1. send message to admin
    #TODO 2. send message to channel in new def
    await bot.send_message(config.CHANNEL_ID,text='OK!')



