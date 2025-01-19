from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import static.funcs as fs

import os

load_dotenv()

prof_router = Router()

@prof_router.callback_query(F.data == 'profile_from_nick', st.Mono.new_nickname)
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ ПРОФИЛЯ', reply_markup=kb.profile)
    await callback.message.delete()
    await state.set_state(st.Mono.main_menu)

@prof_router.callback_query(F.data == 'profile_from_nick')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

@prof_router.callback_query(F.data == 'mono_profile')
async def open_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ТЕКСТ ПРОФИЛЯ', reply_markup=kb.profile)
    await state.set_state(st.Mono.profile)

@prof_router.callback_query(F.data == 'change_nickname')
async def change_nick_begin(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ВВЕДИТЕ НОВЫЙ НИК', reply_markup=kb.awaiting_for_nickname)
    await state.set_state(st.Mono.new_nickname)

@prof_router.message(st.Mono.new_nickname)
async def save_new_name(message: Message, state: FSMContext):
    await rq.change_nick(message.from_user.id, message.text)
    await state.set_state(st.Mono.profile)
    await message.answer('ВАШ НИК ИЗМЕНЕН', reply_markup=kb.profile)




@prof_router.callback_query(F.data == 'change_icons')
async def access_to_icons_check(callback: CallbackQuery, state: FSMContext):
    try:
        icons_access = await rq.icons_get(callback.from_user.id)
    except Exception:
        await callback.message.delete()
        await callback.message.answer('ОШИБКА ПОЛУЧЕНИЯ ДОСТУПА К ИКОНКАМ', reply_markup=kb.profile)
        await state.set_state(st.Mono.profile)
    else:
        await callback.message.delete()
        await callback.message.answer('ВЫБЕРИТЕ ИКОНКУ', reply_markup=kb.icons)
        await state.update_data(access = fs.decode(icons_access))
        await state.set_state(st.Mono.change_icon)

@prof_router.callback_query(st.Mono.change_icon, F.data.startswith('icon_'))
async def save_icon(callback: CallbackQuery, state: FSMContext):
    access = await state.get_data()
    accessed_icons = access["access"]
    icon_id = int(callback.data.split('_')[1]) - 1

    await callback.message.delete()

    if fs.own(icon_id, accessed_icons):
        try:
            await rq.icon_change(_chat_id = callback.from_user.id, _icon_id = icon_id)
        except Exception:
            await callback.message.answer('ОШИБКА УСТАНОВКИ ИКОНКИ', reply_markup=kb.profile)
        else:
            await callback.message.answer('ИЗМЕНЕНИЯ СОХРАНЕНЫ', reply_markup=kb.profile)
    else:
            await callback.message.answer('НЕТ ДОСТУПА К ИКОНКЕ', reply_markup=kb.profile)
