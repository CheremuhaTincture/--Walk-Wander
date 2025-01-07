from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

import os

load_dotenv()

prof_router = Router()

@prof_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('ПРИВЕТСТВИЕ', reply_markup=kb.main_menu)
    await state.set_state(st.mono.main_menu)