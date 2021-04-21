from aiogram.dispatcher.filters.state import State, StatesGroup


class Comment(StatesGroup):
    pages: State = State()
    vote: State = State()


class Stock(StatesGroup):
    stock: State = State()
    Q1: State = State()
    Q2: State = State()
    Q3: State = State()
    Q4: State = State()
    Q5: State = State()
    buy: State = State()


class Edit(StatesGroup):
    Q1: State = State()
    Q2: State = State()
    Q3: State = State()
    Q4: State = State()
    Q5: State = State()


class Delete(StatesGroup):
    Q1: State = State()


class Channel(StatesGroup):
    Q1: State = State()
