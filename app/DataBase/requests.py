from app.DataBase.models import async_session
from app.DataBase.models import User
from sqlalchemy import select, update
from random import randint

async def is_registered(chat_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == chat_id))

        if not user:
            return False
        else:
            return True

async def add_user(user_info):
    async with async_session() as session:
        session.add(User(
            chat_id = user_info["chat_id"],
            name = user_info["name"],
            icons_id = randint(0, 2),
        ))
        await session.commit()