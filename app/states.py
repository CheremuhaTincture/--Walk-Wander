from aiogram.fsm.state import State, StatesGroup

class mono(StatesGroup):
    main_menu = State()
    text_to_support = State()
    profile = State()

class mono_start_reg(StatesGroup):
    name = State()