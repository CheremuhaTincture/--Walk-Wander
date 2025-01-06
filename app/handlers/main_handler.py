from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('ПРИВЕТСТВИЕ')
    await state.set_state(st.mono.main_menu)