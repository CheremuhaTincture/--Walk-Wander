from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton
)

main_menu = InlineKeyboardMarkup(
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

awaiting_for_text = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='В главное меню', callback_data='menu_mono_from_support')
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