from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

reg_router = Router()

async def reg_init(message: Message, state: FSMContext, chat_id: int):
    await message.answer('ПРИВЕТСТВИЕ, НАПИШИ ИМЯ')
    await state.set_state(st.mono_start_reg.name)
    await state.update_data(chat_id = chat_id)

@reg_router.message(st.mono_start_reg.name)
async def save_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(st.mono.main_menu)
    user_info = await state.get_data()
    await rq.add_user(user_info)
    await message.answer('ТЕКСТ МЕНЮ ИЗ РЕГИСТРАЦИИ', reply_markup=kb.main_menu)