from dotenv import load_dotenv
from aiogram.types import Message

import os

import static.funcs as fs
import app.DataBase.requests as rq
import app.keyboards.keyboards as kb
import aiogram.exceptions as ae

def game_lobby(_key, _game_info, new_player_name, player_exit_name, player_erased_name, everybody_are_ready, prev_text):
    map_name = fs.map_name(_game_info['map_id'])
    map_size = fs.map_size(_game_info['map_size'])
    status = fs.game_status(_game_info['status'])
    num_of_players = _game_info['num_of_players']
    if not prev_text:
        text = f'Добро пожаловать в игру №{_key}! Ждем всех игроков, начинаем по команде организатора игры!\n'
        text += f'----------------------\nИнформация об игре:\nКарта: {map_name}\n'
        text += f'Размер карты: {map_size}\nСтатус игры: {status}\n----------------------\n'
        text += f'----------------------\nТекущее число игроков: {num_of_players}\nОжидание игроков...🕝'
    else:
        text0 = prev_text.split('----------------------')[0] + '----------------------\n'
        text1 = prev_text.split('----------------------')[1] + '----------------------'
        text_changed1 = prev_text.split('----------------------')[2]
        if new_player_name != None:
            text_changed1 += f'Игрок {new_player_name} присоединился(лась)!\n'
        if player_exit_name != None:
            text_changed1 += f'Игрок {player_exit_name} покинул(ла) лобби!\n'
        if player_exit_name != None:
            text_changed1 += f'Игрок {player_erased_name} покинул(ла) игру!\n'
        text_changed1 += '----------------------\n'
        if everybody_are_ready and (num_of_players != 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nВсе готовы, можем начинать!⚔️'
        if everybody_are_ready and (num_of_players == 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nОжидание игроков...🕝'
        if (not everybody_are_ready) and (num_of_players != 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nОжидание готовности игроков...🕝'
        text = text0 + text1 + text_changed1 + text_changed2
    return text

async def get_sample_message_text(__key, message: Message):
    _message_id = await rq.get_message_id(__key)

    msg = await message.bot.forward_message(chat_id=int(os.getenv('SPAM_GROUP')),
                                      from_chat_id=int(os.getenv('SPAM_GROUP')),
                                      message_id=_message_id)
    
    return msg.text

async def change_text(__key, _text, message: Message):
    message_n_chat_ids = await rq.get_main_message_ids(__key)

    for id in message_n_chat_ids:
        try:
            if await rq.player_is_admin(id.split('_')[1], __key):
                await message.bot.edit_message_text(message_id=id.split('_')[0],
                                                    chat_id=id.split('_')[1],
                                                    text=_text,
                                                    reply_markup = await kb.game_management_menu_keys(_key=__key))
            else:
                await message.bot.edit_message_text(message_id=id.split('_')[0],
                                                    chat_id=id.split('_')[1],
                                                    text=_text,
                                                    reply_markup=kb.back_to_menu_from_lobby)
        except ae.TelegramBadRequest:
            continue