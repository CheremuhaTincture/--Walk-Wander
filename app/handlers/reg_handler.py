from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from static.text_funcs import static_text

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

reg_router = Router()

async def reg_init(message: Message, state: FSMContext, chat_id: int):
    await message.answer(text = static_text['first_visit'])
    await state.set_state(st.MonoStartReg.name)
    await state.update_data(chat_id = chat_id)

@reg_router.message(st.MonoStartReg.name)
async def save_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(st.Mono.main_menu)
    user_info = await state.get_data()
    await rq.add_user(user_info)
    await message.answer(text = static_text["menu_from_reg"], reply_markup=kb.main_menu(False))