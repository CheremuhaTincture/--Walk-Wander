from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.main_handler import main_router
from app.handlers.profile_handler import prof_router
from app.DataBase.models import async_main

import os, asyncio

load_dotenv()

bot = Bot(token = os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(main_router)
    dp.include_router(prof_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('session terminated.')