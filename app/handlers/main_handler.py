from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.DataBase.requests as rq

main_router = Router()

chat_id = 0

@main_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Я очередной пробирочный бот Славы')