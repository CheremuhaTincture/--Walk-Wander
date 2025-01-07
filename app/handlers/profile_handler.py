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

@prof_router.callback_query(F.data == 'profile_from_nick', st.mono.new_nickname)
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ ПРОФИЛЯ', reply_markup=kb.profile)
    await callback.message.delete()
    await state.set_state(st.mono.main_menu)

@prof_router.callback_query(F.data == 'profile_from_nick')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

@prof_router.callback_query(F.data == 'mono_profile')
async def open_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ТЕКСТ ПРОФИЛЯ', reply_markup=kb.profile)
    await state.set_state(st.mono.profile)

@prof_router.callback_query(F.data == 'change_nickname')
async def change_nick_begin(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ВВЕДИТЕ НОВЫЙ НИК', reply_markup=kb.awaiting_for_nickname)
    await state.set_state(st.mono.new_nickname)

@prof_router.message(st.mono.new_nickname)
async def save_new_name(message: Message, state: FSMContext):
    await rq.change_nick(message.from_user.id, message.text)
    await state.set_state(st.mono.profile)
    await message.answer('ВАШ НИК ИЗМЕНЕН', reply_markup=kb.profile)