from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

game_set_router = Router()

async def game_create_init(callback: CallbackQuery, state: FSMContext):
    try:
        key = await rq.create_game(callback.from_user.id)
    except Exception:
        await callback.message.delete()
        await callback.message.answer('ОШИБКА СОЗДАНИЯ ИГРЫ', reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)
    else:
        await state.set_state(st.MonoGameSetup.map)
        await callback.message.answer('ВЫБОР КАРТЫ',
                                      reply_markup = await kb.maps_keys(_key=key, scnd_time=False))
        await callback.message.delete()

@game_set_router.callback_query(st.MonoGameSetup.map, F.data.startswith('map_'))
async def map_save(callback: CallbackQuery, state: FSMContext):
    await state.update_data(map = callback.data.split('_')[1])
    game_info = await state.get_data()
    key = callback.data.split('_')[2]

    try:
        await rq.update_game(_key=key, _game_info=game_info)
    except Exception:
        await callback.message.delete()
        await callback.message.answer('ОШИБКА СОХРАНЕНИЯ ДАННЫХ', reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)
    else:
        await state.set_state(st.MonoGameManage.menu)
        await callback.message.delete()
        await callback.message.answer(f'ИГРА СОЗДАНА, КЛЮЧ ИГРЫ: {key}',
                                      reply_markup = await kb.game_management_menu_keys(_key=key))




@game_set_router.callback_query(st.MonoGameManage.menu, F.data.startswith('game_reset_'))
async def game_reset_init(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(st.MonoGameManage.reset_map)
    key = callback.data.split('_')[2]
    await callback.message.answer('ВЫБОР КАРТЫ',
                                  reply_markup = await kb.maps_keys(_key=key, scnd_time=True))
    
@game_set_router.callback_query(st.MonoGameManage.reset_map, F.data.startswith('back_to_'))
async def back_to_manage_from_map_reset(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('_')[2]
    await state.set_state(st.MonoGameManage.menu)
    await callback.message.delete()
    await callback.message.answer(f'СНОВА К ИГРЕ, КЛЮЧ ИГРЫ: {key}',
                                  reply_markup = await kb.game_management_menu_keys(_key=key))
    
@game_set_router.callback_query(st.MonoGameManage.reset_map, F.data.startswith('map_'))
async def map_save(callback: CallbackQuery, state: FSMContext):
    await state.update_data(map = callback.data.split('_')[1])
    game_info = await state.get_data()
    key = callback.data.split('_')[2]

    try:
        await rq.update_game(_key=key, _game_info=game_info)
    except Exception:
        await callback.message.delete()
        await callback.message.answer('ОШИБКА СОХРАНЕНИЯ ДАННЫХ', reply_markup=kb.main_menu)
        await state.set_state(st.Mono.main_menu)
    else:
        await state.set_state(st.MonoGameManage.menu)
        await callback.message.delete()
        await callback.message.answer(f'ПАРАМЕТРЫ ИЗМЕНЕНЫ, КЛЮЧ ИГРЫ: {key}',
                                      reply_markup = await kb.game_management_menu_keys(_key=key))

@game_set_router.callback_query(st.MonoGameManage.menu, F.data.startswith('game_begin_'))
async def start_game(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('_')[2]

    try:
        player_count = await rq.player_count(key)
    except Exception:
        await callback.message.delete()
        await callback.message.answer('ОШИБКА ПОДСЧЕТА ИГРОКОВ',
                                      reply_markup = await kb.game_management_menu_keys(_key=key))
    else:
        if player_count > 1:
            try:
                rq.set_game_status_started(key)
            except Exception:
                await callback.message.delete()
                await callback.message.answer('ОШИБКА НАЗНАЧЕНИЯ СТАТУСА',
                                              reply_markup = await kb.game_management_menu_keys(_key=key))
            #else:

        else:
            await callback.answer('Невозможно создать игру без игроков', show_alert=True)

'''@game_set_router.callback_query(st.MonoGameManage.menu, F.data.startswith('t_pl_'))
async def start_game(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split('_')[2]

    print(await rq.player_count(key))
    
    #else:'''