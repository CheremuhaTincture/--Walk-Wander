from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton
)

import app.DataBase.requests as rq
import static.funcs as fs

my_g_kb_router = Router()

async def my_games_keyboard(_page_no, _chat_id):
    games = await rq.get_my_games(_chat_id)

    games_keys = []

    if len(games) != 0:
        if (len(games) % 6) == 0:
            max_page = len(games) // 6 - 1
        else:
            max_page = len(games) // 6
        
        for i in range(_page_no*6, min(len(games), (_page_no + 1)*6)):
            game_key = [
                InlineKeyboardButton(text=f'Игра №{games[i]}',
                                    callback_data=f'game_{games[i]}')
            ]
            games_keys.append(game_key)
        
        control_keys = []

        if _page_no > 0:
            left_key = InlineKeyboardButton(text='⬅️', callback_data=f'my_g_left-{_page_no}')
        else:
            left_key = InlineKeyboardButton(text='⏹️', callback_data='null')
        control_keys.append(left_key)

        middle_key = InlineKeyboardButton(text=f'{_page_no+1}/{max_page+1}', callback_data='null')
        control_keys.append(middle_key)

        back_key = InlineKeyboardButton(text='Назад', callback_data='mono_profile')
        control_keys.append(back_key)

        if _page_no < max_page:
            right_key = InlineKeyboardButton(text='➡️', callback_data=f'my_g_right-{_page_no}')
        else:
            right_key = InlineKeyboardButton(text='⏹️', callback_data='null')
        control_keys.append(right_key)
    else:
        control_keys = [
            InlineKeyboardButton(text='🏠У вас еще нет игр🏠', callback_data='mono_profile')
        ]

    games_keys.append(control_keys)

    return InlineKeyboardMarkup(row_wigth = 1, inline_keyboard=games_keys)

@my_g_kb_router.callback_query(F.data.startswith('my_g_left-'))
async def page_left(callback: CallbackQuery):
    page_no = callback.data.split('-')[1] - 1
    
    await callback.answer()
    await callback.message.edit_text(text='ВОТ ВАШИ ИГРЫ', 
                                     reply_markup = await my_games_keyboard(_page_no = page_no,
                                                                            _chat_id=callback.from_user.id))

@my_g_kb_router.callback_query(F.data.startswith('my_g_right'))
async def page_left(callback: CallbackQuery):
    page_no = callback.data.split('-')[1] + 1
    
    await callback.answer()
    await callback.message.edit_text(text='ВОТ ВАШИ ИГРЫ', 
                                     reply_markup = await my_games_keyboard(_page_no = page_no,
                                                                            _chat_id=callback.from_user.id))
