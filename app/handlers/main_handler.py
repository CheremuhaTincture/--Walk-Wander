from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from app.handlers.reg_handler import reg_init
from app.handlers.game_manage_handler import game_create_init

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import static.funcs as fs

import os

load_dotenv()

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await rq.is_registered(message.from_user.id):
        await message.answer('ПРИВЕТСТВИЕ', reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)
    else:
        await reg_init(message, state, message.from_user.id)

@main_router.callback_query(F.data == 'menu_mono_from_support', st.Mono.text_to_support)
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ МЕНЮ', reply_markup=kb.main_menu)
    await callback.message.delete()
    await state.set_state(st.Mono.main_menu)

@main_router.callback_query(F.data == 'menu_mono_from_support')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

@main_router.callback_query(F.data == 'menu_mono')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ МЕНЮ', reply_markup=kb.main_menu)
    await callback.message.delete()
    await state.set_state(st.Mono.main_menu)

@main_router.callback_query(F.data == 'menu_mono_from_lobby')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await rq.deactivate_player(callback.from_user.id)
    await callback.message.answer('ТЕКСТ МЕНЮ', reply_markup=kb.main_menu)
    await callback.message.delete()
    await state.set_state(st.Mono.main_menu)




@main_router.callback_query(F.data == 'mono_support')
async def mono_support(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ТЕКСТ ПОДДЕРЖКИ', reply_markup=kb.awaiting_for_text)
    await callback.message.delete()
    await state.set_state(st.Mono.text_to_support)

@main_router.message(st.Mono.text_to_support)
async def sending_text(message: Message, state: FSMContext):
    await state.set_state(st.Mono.main_menu)
    await message.answer('ТЕКСТ ОТПРАВКИ', reply_markup=kb.main_menu)
    await message.bot.send_message(chat_id=int(os.getenv('SUPPORT_GROUP')),
                                   text=f'Сообщение от пользователя {message.from_user.id}:\n\n'+message.text)

@main_router.message(F.text.contains('_'))
async def support_answer(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        chat_id = int(message.text.split('_')[0])
        text = message.text.split('_')[1]
        await message.bot.send_message(chat_id=chat_id,
                                    text='Ответ от поддержки!\n\n'+text)
        



@main_router.callback_query(F.data == 'mono_new')
async def new_game(callback: CallbackQuery, state: FSMContext):
    await game_create_init(callback=callback, state=state)

@main_router.callback_query(F.data == 'mono_code')
async def enter_by_code(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('ВВЕДИТЕ КОД ИГРЫ', reply_markup=kb.back_to_menu)
    await state.set_state(st.Mono.game_key)

@main_router.message(st.Mono.game_key)
async def check_key(message: Message, state: FSMContext):
    if (len(message.text) == 3) and (message.text.isdigit()):
        key = message.text
        try:
            game_info = await rq.get_game_info(key)
            if await rq.game_is_created(key):
                await rq.join_game(message.from_user.id, key)
                map_name = fs.map_name(game_info['map_id'])
                map_size = fs.map_size(game_info['map_size'])
                status = fs.game_status(game_info['status'])
                if await rq.player_is_admin(message.from_user.id, key):
                    await message.answer(f'ВЫ ПОДКЛЮЧИЛИСЬ К ВАШЕЙ ИГРЕ №{key}\nКарта: {map_name}\nРазмер карты: {map_size}\nСтатус игры: {status}\nЧисло игроков: {game_info['num_of_players']}',
                                        reply_markup = await kb.game_management_menu_keys(_key=key))
                else:
                    await message.answer(f'ВЫ ПОДКЛЮЧИЛИСЬ К ИГРЕ №{key}\nКарта: {map_name}\nРазмер карты: {map_size}\nСтатус игры: {status}\nЧисло игроков: {game_info['num_of_players']}',
                                         reply_markup=kb.back_to_menu_from_lobby)
            else:
                await message.answer('К ЭТОЙ ИГРЕ ПРИСОЕДИНИТЬСЯ УЖЕ НЕЛЬЗЯ',
                                     reply_markup=kb.main_menu)

        except Exception:
            await message.answer('ОШИБКА ПРИ ПРИСОЕДИНЕНИИ',
                                 reply_markup=kb.main_menu)
            
        await state.clear()
    else:
        await message.answer('ВВЕДИТЕ КОРРЕКТНЫЙ КОД')
        


@main_router.callback_query(F.data == 'null')
async def null_func(callback: CallbackQuery):
    await callback.answer()