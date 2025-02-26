from aiogram import Bot
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Mono(StatesGroup):
    main_menu = State()
    text_to_support = State()
    profile = State()
    new_nickname = State()
    change_icon = State()
    game_key = State()

class MonoStartReg(StatesGroup):
    name = State()

class MonoGameSetup(StatesGroup):
    map = State()

class MonoGameManage(StatesGroup):
    menu = State()
    reset_map = State()

class MonoGameplay(StatesGroup):
    turn = State()
    wait = State()

async def give_state(chat_id, bot_id, state: State, storage):
    state_with: FSMContext = FSMContext(
                storage=storage,
                key=StorageKey(
                    chat_id=chat_id,
                    user_id=chat_id,
                    bot_id=bot_id))
    await state_with.set_state(state)
    print(await state_with.get_state())

async def get_state(chat_id, bot_id, storage):
    state_with: FSMContext = FSMContext(
                storage=storage,
                key=StorageKey(
                    chat_id=chat_id,
                    user_id=chat_id,
                    bot_id=bot_id))
    print(await state_with.get_state())