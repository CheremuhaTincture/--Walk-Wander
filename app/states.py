from aiogram.fsm.state import State, StatesGroup

class mono(StatesGroup):
    main_menu = State()
    text_to_support = State()