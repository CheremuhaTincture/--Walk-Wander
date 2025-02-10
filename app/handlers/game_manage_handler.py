from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from static.text_funcs import static_text

import os

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import static.funcs as fs
import static.text_funcs as tf

load_dotenv()

game_set_router = Router()

async def game_create_init(callback: CallbackQuery, state: FSMContext):
    """try:
        key = await rq.create_game(callback.from_user.id)
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["game_creating_err"], reply_markup=kb.main_menu(False))
        await state.set_state(st.Mono.main_menu)
    else:"""
    await state.set_state(st.MonoGameSetup.map)
    await callback.message.answer(text=static_text["choose_map"],
                                    reply_markup = await kb.maps_keys(_key=None, scnd_time=False))
    await callback.message.delete()

@game_set_router.callback_query(st.MonoGameSetup.map, F.data.startswith('map_'))
async def map_save(callback: CallbackQuery, state: FSMContext):
    await state.update_data(map_id = callback.data.split('_')[1])
    game_info = await state.get_data()

    try:
        key = await rq.create_game(callback.from_user.id, game_info)

    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["game_creating_err"], reply_markup=kb.main_menu(False))
        await state.set_state(st.Mono.main_menu)

    else:
        await state.set_state(st.MonoGameManage.menu)
        await callback.message.delete()

        game_info = await rq.get_game_info(key)
        sample_message_text = tf.game_lobby(key, game_info, None, None, None,
                                          await rq.everybody_are_ready(key),
                                          None)

        sample_message = await callback.bot.send_message(text=sample_message_text,
                                                         chat_id=os.getenv('SPAM_GROUP'))
        sample_message_id = sample_message.message_id

        msg = await callback.message.answer(
            text=sample_message_text,
            reply_markup = await kb.game_management_menu_keys(_key=key)
        )
        
        await rq.set_sample_message_id(key, sample_message_id)
        await rq.set_main_message(callback.from_user.id, key, msg.message_id)




@game_set_router.callback_query(st.MonoGameManage.menu, F.data.startswith('game_reset_'))
async def game_reset_init(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(st.MonoGameManage.reset_map)
    key = callback.data.split('_')[2]
    await callback.message.answer(text=static_text["choose_map"],
                                  reply_markup = await kb.maps_keys(_key=key, scnd_time=True))
    
#Вернуться к игре, не изменяя карту
@game_set_router.callback_query(st.MonoGameManage.reset_map, F.data.startswith('back_to_'))
async def back_to_manage_from_map_reset(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.MonoGameManage.menu)
    await callback.message.delete()
    key = callback.data.split('_')[2]
    message = callback.message

    try:
        game_info = await rq.get_game_info(_key=key)
        old_text = await tf.get_sample_message_text(key, message)

        sample_message_text = tf.game_lobby(
            key, 
            game_info,
            None,
            None,
            None, 
            await rq.everybody_are_ready(key),
            old_text
        )

        msg = await message.answer(
            text=sample_message_text,
            reply_markup = await kb.game_management_menu_keys(_key=key)
        )
        await rq.set_main_message(callback.from_user.id, key, msg.message_id)

        await tf.change_text(key, sample_message_text, message)

        sample_message = await message.bot.send_message(text=sample_message_text,
                                                chat_id=os.getenv('SPAM_GROUP'))
        sample_message_id = sample_message.message_id
        await rq.set_sample_message_id(key, sample_message_id)

    except Exception:
        await message.answer(text=static_text["game_returning_err"],
                            reply_markup=kb.main_menu(False))
    
@game_set_router.callback_query(st.MonoGameManage.reset_map, F.data.startswith('map_'))
async def map_save(callback: CallbackQuery, state: FSMContext):
    await state.update_data(map_id = callback.data.split('_')[1])
    game_info = await state.get_data()
    key = callback.data.split('_')[2]

    try:
        await rq.update_game(_key=key, _game_info=game_info)
        game_info = await rq.get_game_info(_key=key)
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["saving_data_err"], reply_markup=kb.main_menu(False))
        await state.set_state(st.Mono.main_menu)
    else:
        await state.set_state(st.MonoGameManage.menu)
        await callback.message.delete()
        message = callback.message
        try:
            old_text = await tf.get_sample_message_text(key, message)

            sample_message_text = tf.game_lobby(
                key, 
                game_info,
                None,
                None,
                None, 
                await rq.everybody_are_ready(key),
                old_text
            )

            msg = await message.answer(
                text=sample_message_text,
                reply_markup = await kb.game_management_menu_keys(_key=key)
            )
            await rq.set_main_message(callback.from_user.id, key, msg.message_id)

            await tf.change_text(key, sample_message_text, message)

            sample_message = await message.bot.send_message(text=sample_message_text,
                                                    chat_id=os.getenv('SPAM_GROUP'))
            sample_message_id = sample_message.message_id
            await rq.set_sample_message_id(key, sample_message_id)

        except Exception:
            await message.answer(text=static_text["game_returning_err"],
                                reply_markup=kb.main_menu(False))




@game_set_router.callback_query(st.MonoGameManage.menu, F.data.startswith('game_begin_'))
async def start_game(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('_')[2]

    #считаем игроков и готовность всех игроков:
    try:
        player_count = await rq.player_count(key)
        everybody_are_ready = await rq.everybody_are_ready(key)

    except Exception:
        await callback.message.delete()
        await callback.message.answer(text=static_text["players_counting_err"],
                                      reply_markup = await kb.game_management_menu_keys(_key=key))
        
    else:
        if (player_count > 1) and (everybody_are_ready):
            try:
                await rq.set_game_status_started(key)

            except Exception:
                await callback.message.delete()
                await callback.message.answer(text=static_text["status_giving_err"],
                                              reply_markup = await kb.game_management_menu_keys(_key=key))
                
            #else:

        if not everybody_are_ready:
            await callback.answer('Кто-то из игроков не зашел в лобби', show_alert=True)
        if player_count == 0:
            await callback.answer('Невозможно создать игру без игроков', show_alert=True)