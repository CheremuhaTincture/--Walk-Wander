from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton
)

import app.DataBase.requests as rq

import random

def main_menu(_shuffle: bool):
    if not _shuffle:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⚜️Случайная игра⚜️', callback_data='mono_random')
                ],
                [
                    InlineKeyboardButton(text='🔮Создать🔮', callback_data='mono_new')
                ],
                [
                    InlineKeyboardButton(text='🎟️Присоединиться по коду🎟️', callback_data='mono_code')
                ],
                [
                    InlineKeyboardButton(text='👑Профиль👑', callback_data='mono_profile'),
                    InlineKeyboardButton(text='🔱Поддержка🔱', callback_data='mono_support')
                ]
            ]
        )
    else:
            button1 = InlineKeyboardButton(text='⚜️Случайная игра⚜️', callback_data='mono_random')
            button2 = InlineKeyboardButton(text='🔮Создать🔮', callback_data='mono_new')
            button3 = InlineKeyboardButton(text='🎟Присоединиться по коду🎟', callback_data='mono_code')
            button4 = InlineKeyboardButton(text='👑Профиль👑', callback_data='mono_profile')
            button5 = InlineKeyboardButton(text='🔱Поддержка🔱', callback_data='mono_support')

            buttons = [button1, button2, button4, button5]
            
            random.shuffle(buttons)

            string_of_two_buttons = []
            string_of_two_buttons.extend(buttons[:2])
            buttons.append(button3)
            keys = [string_of_two_buttons]

            for i in range(2, 5):
                keys.append([buttons[i]])
            
            random.shuffle(keys)
            
            return InlineKeyboardMarkup(inline_keyboard=keys) 
        

back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='В главное меню', callback_data='menu_mono')
        ]
    ]
)

awaiting_for_text = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='В главное меню', callback_data='menu_mono_from_support')
        ]
    ]
)

awaiting_for_nickname = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить', callback_data='profile_from_nick')
        ]
    ]
)

profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔱Изменить Значки🔱', callback_data='change_icons')
        ],
        [
            InlineKeyboardButton(text='⚜️Изменить Имя⚜️', callback_data='change_nickname')
        ],
        [
            InlineKeyboardButton(text='🔮Мои игры🔮', callback_data='my_games')
        ],
        [
            InlineKeyboardButton(text='🏠В меню🏠', callback_data='menu_mono')
        ]
    ]
)

def gameplay_menu(_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Сделать ход 🎲', callback_data=f'dice_rolled_{_key}')
            ]
        ]
    )

async def icons(__chat_id):
    icon_id = await rq.chosen_icon(_chat_id=__chat_id)

    keys = []

    for i in range(0, 2):
        if icon_id == i:
            keys.append(
                [
                    InlineKeyboardButton(text=f'✨Иконка {i+1}✨', callback_data=f'icon_{i+1}')
                ]
            )
        else:
            keys.append(
                [
                    InlineKeyboardButton(text=f'Иконка {i+1}', callback_data=f'icon_{i+1}')
                ]
            )

    keys.append(
        [
            InlineKeyboardButton(text='👑Назад👑', callback_data='mono_profile')
        ]
    )

    return InlineKeyboardMarkup(row_wigth = 1, inline_keyboard=keys)

async def maps_keys(_key, scnd_time):  
    keys = [
        [
            InlineKeyboardButton(text='🏰Карта 1🏰', callback_data=f'map_1_{_key}')
        ]
        #[
        #    InlineKeyboardButton(text='🏜️Карта 2🏜️', callback_data=f'map_2_{_key}')
        #]
    ]

    if not scnd_time:
        keys.append(
            [
                InlineKeyboardButton(text='🏠В меню🏠', callback_data=f'menu_mono')
            ]
        )
    else:
        keys.append(
            [
                InlineKeyboardButton(text='🔮Назад🔮', callback_data=f'back_to_{_key}')
            ]
        )
    
    return InlineKeyboardMarkup(row_wigth = 1, inline_keyboard=keys)

'''size_of_map = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Маленькая', callback_data='map_size_s')
        ],
        [
            InlineKeyboardButton(text='Стандартная', callback_data='map_size_m')
        ],
        [
            InlineKeyboardButton(text='Большая', callback_data='map_size_l')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='map_choose')
        ],
        [
            InlineKeyboardButton(text='🏠В меню🏠', callback_data='menu_mono')
        ]
    ]
)'''

async def game_management_menu_keys(_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🚩Начать игру🚩', callback_data=f'game_begin_{_key}')
            ],
            [
                InlineKeyboardButton(text='🔱Изменить настройки🔱', callback_data=f'game_reset_{_key}')
            ],
            #[
            #    InlineKeyboardButton(text='_тест списка игроков_', callback_data=f't_pl_{_key}')
            #],
            [
                InlineKeyboardButton(text='🏠Сохранить и выйти🏠', callback_data='menu_mono')
            ]
        ]
    )

async def game_management_m_g_keys(_key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🚩Войти в игру🚩', callback_data=f'game_enter-{_key}')
            ],
            [
                InlineKeyboardButton(text='❌Стереть информацию❌', callback_data=f'game_erase-{_key}')
            ],
            [
                InlineKeyboardButton(text='🔮Назад🔮', callback_data='my_games')
            ]
        ]
    )

async def back_to_menu_from_lobby(key):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='В главное меню', callback_data=f'menu_mono_from_lobby-{key}')
            ]
        ]
    )