from aiogram.dispatcher.filters.state import State, StatesGroup


class Comment(StatesGroup):
    pages: State = State()
    vote: State = State()

class Stock(StatesGroup):
    stock: State = State()
    name: State = State()
    description: State = State()
    price: State = State()
    photo: State = State()
    submit: State = State()
    buy: State = State()