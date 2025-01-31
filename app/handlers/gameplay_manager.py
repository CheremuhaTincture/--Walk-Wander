from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import app.keyboards.keyboards as kb
import app.DataBase.requests as rq
import app.states as st

import os

load_dotenv()

gameplay_router = Router()