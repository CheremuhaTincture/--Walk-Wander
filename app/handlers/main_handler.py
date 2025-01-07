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

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('ПРИВЕТСТВИЕ', reply_markup=kb.main_menu)
    await state.set_state(st.mono.main_menu)

@main_router.callback_query(F.data == 'menu_mono')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ МЕНЮ', reply_markup=kb.main_menu)
    await callback.message.delete()
    await state.set_state(st.mono.main_menu)





@main_router.callback_query(F.data == 'mono_support')
async def mono_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ ПОДДЕРЖКИ', reply_markup=kb.awaiting_for_text)
    await callback.message.delete()
    await state.set_state(st.mono.text_to_support)

@main_router.message(st.mono.text_to_support)
async def sending_text(message: Message, state: FSMContext):
    await message.bot.send_message(chat_id=int(os.getenv('SUPPORT_GROUP')),
                                   text=f'Сообщение от пользователя {message.from_user.id}:\n\n'+message.text)

@main_router.message(F.text.contains('_'))
async def support_answer(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        chat_id = int(message.text.split('_')[0])
        text = message.text.split('_')[1]
        await message.bot.send_message(chat_id=chat_id,
                                    text='Ответ от поддержки!\n\n'+text)