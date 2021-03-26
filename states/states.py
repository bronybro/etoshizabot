from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Comment(StatesGroup):
    cs: State = State()
    vote: State = State()