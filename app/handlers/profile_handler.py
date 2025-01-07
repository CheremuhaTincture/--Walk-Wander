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

@prof_router.callback_query(F.data == 'mono_profile')
async def open_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ТЕКСТ ПРОФИЛЯ', reply_markup=kb.profile)
    await state.set_state(st.mono.profile)

