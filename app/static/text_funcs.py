from aiogram.types import Message, FSInputFile
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from dotenv import load_dotenv
from random import randint
from app.states import give_state, MonoGameplay

import os
import json
import asyncio

import app.static.funcs as fs
import app.DataBase.requests as rq
import app.keyboards.keyboards as kb
import aiogram.exceptions as ae
import app.image as img



with open("app/static/texts.json", "r", encoding="utf8") as st:
    static_text = json.load(st)



#ПОЛУЧЕНИЕ ТЕКСТА ГЛАВНОГО СООБЩЕНИЯ ИГРЫ (КОСТЫЛЬ ПИЗДЕЦ)
async def get_sample_message_text(__key, message: Message):
    _message_id = await rq.get_message_id(__key)

    msg = await message.bot.forward_message(chat_id=int(os.getenv('SPAM_GROUP')),
                                      from_chat_id=int(os.getenv('SPAM_GROUP')),
                                      message_id=_message_id)
    
    return msg.text



async def change_text_lobby(__key, _text, message: Message):
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
                                                    reply_markup = await kb.back_to_menu_from_lobby(__key))
        except ae.TelegramBadRequest:
            continue

async def change_lobby_text_to_gameplay(_key, _text, map_id, message: Message, state_storage):
    message_n_chat_ids = await rq.get_main_message_ids_n_index(_key)

    turn = await rq.get_turn(_key)

    path = await img.generate_game_field(map_id, _key)

    gf = FSInputFile(path)

    for id in message_n_chat_ids:
        ids=id.split('_')
        await message.bot.delete_message(message_id=ids[0],
                                         chat_id=ids[1])
        main_msg = await message.bot.send_photo(chat_id=ids[1],
                                                caption=_text,
                                                photo = gf)
        if int(ids[2]) == turn:
            event_msg = await message.bot.send_message(chat_id=ids[1],
                                                       text='Ваша очередь ходить',
                                                       reply_markup=kb.gameplay_menu)
        else:
            vent_msg = await message.bot.send_message(chat_id=ids[1],
                                                       text='Ожидание хода оппонента...')
                                                        #reply_markup=ReplyKeyboardRemove())

        sample_message = await message.bot.send_message(text=_text,
                                                        chat_id=os.getenv('SPAM_GROUP'))
        sample_message_id = sample_message.message_id
        await rq.set_sample_message_id(_key, sample_message_id)
        await rq.set_event_n_main_msg(ids[1], _key, event_msg.message_id, main_msg.message_id)

    os.remove(path)



def get_random_menu_text():
    a = randint(1, 100)

    if (a in range(1, 96)):
        index = a // 19 + 1
        return static_text[f'menu{index}'], False
    elif (a in range(96, 99)):
        return static_text['menu6'], True
    else:
        return static_text['menu7'], False



#ТЕКСТ ЛОББИ ИГРЫ
def game_lobby(_key, _game_info, new_player_name, player_exit_name, player_erased_name, everybody_are_ready, prev_text):
    map_name = fs.map_name(_game_info['map_id'])
    map_size = fs.map_size(_game_info['map_size'])
    status = fs.game_status(_game_info['status'])
    num_of_players = _game_info['num_of_players']
    if not prev_text:
        text = f'Добро пожаловать в игру №{_key}! Ждем всех игроков, начинаем по команде организатора игры!\n'
        text += f'——————————————\nИнформация об игре:\nКарта: {map_name}\n'
        text += f'Размер карты: {map_size}\nСтатус игры: {status}\n——————————————\n'
        text += f'——————————————\nТекущее число игроков: {num_of_players}\nОжидание игроков...🕝'
    else:
        text0 = f'Добро пожаловать в игру №{_key}! Ждем всех игроков, начинаем по команде организатора игры!\n——————————————\nИнформация об игре:\nКарта: {map_name}\nРазмер карты: {map_size}\nСтатус игры: {status}\n——————————————'
        text_changed1 = prev_text.split('——————————————')[2]
        if new_player_name != None:
            text_changed1 += f'Игрок {new_player_name} присоединился(лась)!\n'
        elif player_exit_name != None:
            text_changed1 += f'Игрок {player_exit_name} покинул(ла) лобби!\n'
        elif player_erased_name != None:
            text_changed1 += f'{player_erased_name} покинул(ла) игру!\n'
        text_changed1 += '——————————————\n'
        if everybody_are_ready and (num_of_players != 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nВсе готовы, можем начинать!⚔️'
        if everybody_are_ready and (num_of_players == 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nОжидание игроков...🕝'
        if (not everybody_are_ready) and (num_of_players != 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nОжидание готовности игроков...🕝'
        if (not everybody_are_ready) and (num_of_players == 1):
            text_changed2 = f'Текущее число игроков: {num_of_players}\nНу и куда все ушли?!🤬'
        text = text0 + text_changed1 + text_changed2
    return text



#ТЕКСТ ГЕЙМПЛЕЯ
def gameplay(_key, _game_info, player_exit_name, prev_text: str, current_turn, _players, current_leader):

    map_name = fs.map_name(_game_info['map_id'])
    map_size = fs.map_size(_game_info['map_size'])

    text1 = f'Игра №{_key} началась!\n'
    text2 = '——————————————\n'
    text3 = f'Карта: {map_name}\nРазмер карты: {map_size}\n'
    text4 = '——————————————\n'
    text5 = 'Очередность хода:\n'
    text6 = ''

    for i in range(0, len(_players)):
        if i == current_turn:
            text6 += '⚔️'
        else:
            text6 += '🕝'
        
        text6 += _players[i]

        if i == current_leader:
            text6 += '🏆\n'
        else:
            text6 += '\n'
    
    text7 = '——————————————\n'

    final_text = text1+text2+text3+text4+text5+text6+text7

    if prev_text != None:
        final_text += prev_text.split('——————————————')[3]

    if player_exit_name != None:
        final_text += f'\nИгрок {player_exit_name} покинул(ла) игру!'
    
    return final_text