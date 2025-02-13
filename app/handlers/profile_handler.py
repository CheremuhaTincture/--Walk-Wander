from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from app.keyboards.my_games_keyboard import my_games_keyboard
from static.text_funcs import static_text

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import static.funcs as fs
import static.text_funcs as tf

import os

load_dotenv()

prof_router = Router()

@prof_router.callback_query(F.data == 'profile_from_nick', st.Mono.new_nickname)
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=static_text["profile"], reply_markup=kb.profile)
    await callback.message.delete()
    await state.set_state(st.Mono.main_menu)

@prof_router.callback_query(F.data == 'profile_from_nick')
async def menu_mono(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

@prof_router.callback_query(F.data == 'mono_profile')
async def open_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=static_text["profile"], reply_markup=kb.profile)
    await state.set_state(st.Mono.profile)

@prof_router.callback_query(F.data == 'change_nickname')
async def change_nick_begin(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=static_text["new_nickname"],
                                  reply_markup=kb.awaiting_for_nickname)
    await state.set_state(st .Mono.new_nickname)

@prof_router.message(st.Mono.new_nickname)
async def save_new_name(message: Message, state: FSMContext):
    await rq.change_nick(message.from_user.id, message.text)
    await state.set_state(st.Mono.profile)
    await message.answer(text=static_text["new_nickname_aproved"],
                         reply_markup=kb.profile)




@prof_router.callback_query(F.data == 'change_icons')
async def access_to_icons_check(callback: CallbackQuery, state: FSMContext):
    try:
        icons_access = await rq.icons_get(callback.from_user.id)
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["icon_access_err"],
                                      reply_markup=kb.profile)
        await state.set_state(st.Mono.profile)
    else:
        await callback.message.delete()
        await callback.message.answer(text=static_text["choose_icon"],
                                      reply_markup = await kb.icons(__chat_id = callback.from_user.id))
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
            await callback.message.answer(text=static_text["icon_set_err"],
                                          reply_markup=kb.profile)
        else:
            await callback.message.answer(text=static_text["icon_set"],
                                          reply_markup=kb.profile)
    else:
            await callback.message.answer(text=static_text["no_access"],
                                          reply_markup=kb.profile)




@prof_router.callback_query(F.data == 'my_games')
async def my_games(callback: CallbackQuery):
    await callback.message.delete()

    try:
        await callback.message.answer(text=static_text["my_games"],
                                      reply_markup = await my_games_keyboard(0, callback.from_user.id))
    except Exception:
        await callback.message.answer(text=static_text["games_loading_err"],
                                      reply_markup=kb.profile) 

@prof_router.callback_query(F.data.startswith('game_number-'))
async def get_game(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    key = callback.data.split('-')[1]

    try:
        game_info = await rq.get_game_info(key)
    except Exception:
        await callback.message.answer(text=static_text["game_loading_err"],
                                      reply_markup=kb.profile) 
    else:
        map_name = fs.map_name(game_info['map_id'])
        map_size = fs.map_size(game_info['map_size'])
        status = fs.game_status(game_info['status'])
        await callback.message.answer(f'Карта: {map_name}\nРазмер карты: {map_size}\nСтатус игры: {status}\nЧисло игроков: {game_info['num_of_players']}',
                                      reply_markup = await kb.game_management_m_g_keys(key))

@prof_router.callback_query(F.data.startswith('game_enter-'))
async def return_to_game(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('-')[1]

    try:
        game_info = await rq.get_game_info(key)
        if await rq.game_is_created(key):
            await state.set_state(st.MonoGameManage.menu)
            await callback.message.delete()
                
            old_text = await tf.get_sample_message_text(key, callback.message)
            await rq.join_game(callback.from_user.id, key)

            #Присоединение к игре админа
            if await rq.player_is_admin(callback.from_user.id, key):

                sample_message_text = tf.game_lobby(
                    key, game_info,
                    None,
                    None, None, await rq.everybody_are_ready(key),
                    old_text
                )

                msg = await callback.message.answer(
                    text=sample_message_text,
                    reply_markup = await kb.game_management_menu_keys(_key=key)
                )
                await rq.set_main_message(callback.from_user.id, key, msg.message_id)

            #Присоединение к игре не админа
            else:

                sample_message_text = tf.game_lobby(
                    key, game_info,
                    await rq.get_player_name(callback.from_user.id),
                    None, None, await rq.everybody_are_ready(key),
                    old_text
                )

                msg = await callback.message.answer(
                    text=sample_message_text,
                    reply_markup = await kb.back_to_menu_from_lobby(key)
                )
                await rq.set_main_message(callback.from_user.id, key, msg.message_id)

                await tf.change_text(key, sample_message_text, callback.message)

                sample_message = await callback.bot.send_message(text=sample_message_text,
                                                        chat_id=os.getenv('SPAM_GROUP'))
                sample_message_id = sample_message.message_id
                await rq.set_sample_message_id(key, sample_message_id)
        else:
            await callback.message.delete()
            await callback.message.answer(text=static_text["cant_return"],
                                          reply_markup = await my_games_keyboard(0, callback.from_user.id))
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["game_connection_err"], reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)

@prof_router.callback_query(F.data.startswith('game_erase-'))
async def return_to_game(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('-')[1]

    try:
        old_text = await tf.get_sample_message_text(key, callback.message)
        is_admin = await rq.player_is_admin(callback.from_user.id, key)
        await rq.erase_player(_chat_id=callback.from_user.id, _key=key)
        game_info = await rq.get_game_info(key)
        #Отключение от игры админа
        if is_admin:

            exited_player = 'Организатор ' + await rq.get_player_name(callback.from_user.id)

            sample_message_text = tf.game_lobby(
                key, 
                game_info,
                None,
                None, 
                exited_player, 
                await rq.everybody_are_ready(key),
                old_text
            )

        #Отсоединение от игры не админа
        else:

            exited_player = 'Игрок ' + await rq.get_player_name(callback.from_user.id)

            sample_message_text = tf.game_lobby(
                key, 
                game_info,
                None,
                None, 
                exited_player, 
                await rq.everybody_are_ready(key),
                old_text
            )

        await tf.change_text(key, sample_message_text, callback.message)

        sample_message = await callback.bot.send_message(text=sample_message_text,
                                                         chat_id=os.getenv('SPAM_GROUP'))
        sample_message_id = sample_message.message_id
        await rq.set_sample_message_id(key, sample_message_id)


    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["delete_err"],
                                      reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)
    else:
        await callback.message.delete()
        await callback.message.answer(text=static_text["deleted"],
                                      reply_markup = await my_games_keyboard(0, callback.from_user.id))