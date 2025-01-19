from aiogram.fsm.state import State, StatesGroup

class Mono(StatesGroup):
    main_menu = State()
    text_to_support = State()
    profile = State()
    new_nickname = State()
    change_icon = State()

class MonoStartReg(StatesGroup):
    name = State()

class MonoGameSetup(StatesGroup):
    map = State()

class MonoGameManage(StatesGroup):
    menu = State()
    reset_map = State()