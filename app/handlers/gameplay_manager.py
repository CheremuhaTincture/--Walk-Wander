from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import app.static.text_funcs as tf

import os, asyncio, random

load_dotenv()

gameplay_router = Router()

async def game_start(key, callback: CallbackQuery):
    await callback.answer('Начинаем игру...')
    await callback.message.edit_reply_markup(reply_markup=kb.back_to_menu)

    #СОЗДАНИЕ ОЧЕРЕДНОСТИ ХОДА
    await rq.create_queue(key)

    #ОТПРАВКА СООБЩЕНИЯ О НАЧАЛЕ ИГРЫ
    game_info = await rq.get_game_info(key)

    sample_message_text = await tf.gameplay(
        _key = key, 
        player_exit_name = None,
        prev_text = None,
        current_turn = 0,
        got_coin_text = None
    )

    await tf.change_lobby_text_to_gameplay(key, sample_message_text, game_info["map_id"], callback)

@gameplay_router.callback_query(F.data.startswith('dice_rolled_'))
async def inc_score(callback: CallbackQuery):
    
    #score = random.randint(1, 6)
    score = 1
    
    key = callback.data.split('_')[2]
    
    game_info = await rq.get_game_info(key)
    
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    msg = await callback.message.answer('Бросаем кубик...')
    
    sample_message_text = await tf.gameplay(
        _key = key, 
        player_exit_name = None,
        prev_text = None,
        current_turn = 0,
        got_coin_text = None
    )
    
    got_coin = await rq.change_score(callback.from_user.id, key, score, game_info["map_id"], game_info["map_size"])
    
    task1 = asyncio.create_task(tf.change_text_gameplay(key, sample_message_text, game_info["map_id"], callback))
    await asyncio.gather(task1)
    
    await asyncio.sleep(2)
    await callback.bot.delete_message(chat_id = callback.from_user.id, message_id = msg.message_id)
    await asyncio.sleep(0.25)
    msg = await callback.message.answer(f'Выпало {score}!\nСмеяться или плакать будете потом, а сейчас внимание на игровое поле!')
    await asyncio.sleep(3)
    await callback.bot.delete_message(chat_id = callback.from_user.id, message_id = msg.message_id)