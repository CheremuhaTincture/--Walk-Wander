from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st
import app.static.text_funcs as tf

import os

load_dotenv()

gameplay_router = Router()

async def game_start(key, callback: CallbackQuery):

    #СОЗДАНИЕ ОЧЕРЕДНОСТИ ХОДА
    await rq.create_queue(key)

    #ОТПРАВКА СООБЩЕНИЯ О НАЧАЛЕ ИГРЫ
    game_info = await rq.get_game_info(key)

    queue = await rq.get_queue(key)
    leader = await rq.get_leader(key)

    sample_message_text = tf.gameplay(
        _key = key, 
        _game_info = game_info,
        player_exit_name = None,
        prev_text = None,
        current_turn = 0,
        _players = queue,
        current_leader = leader
    )

    #sample_message = await callback.bot.send_message(text=sample_message_text,
    #                                                 chat_id=os.getenv('SPAM_GROUP'))
    #sample_message_id = sample_message.message_id

    await tf.change_text_lobby_to_gameplay(key, sample_message_text, callback)
    #await rq.set_sample_message_id(key, sample_message_id)