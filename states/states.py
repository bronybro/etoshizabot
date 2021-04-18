from aiogram.dispatcher.filters.state import State, StatesGroup


class Comment(StatesGroup):
    pages: State = State()
    vote: State = State()

class Stock(StatesGroup):
    flag: State = State()
    buy: State = State()