from app.DataBase.models import async_session
from app.DataBase.models import User, Game, Player, Match
from sqlalchemy import select, update
from random import randint

async def is_registered(_chat_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == _chat_id))

        if not user:
            return False
        else:
            return True

async def add_user(user_info):
    async with async_session() as session:
        session.add(User(
            chat_id = user_info["chat_id"],
            name = user_info["name"],
            icons_id = randint(0, 1),
        ))
        await session.commit()

async def change_nick(_chat_id, new_name):
    async with async_session() as session:
        change = (update(User)
                  .where(User.chat_id == _chat_id)
                  .values(name = new_name))
        await session.execute(change)
        await session.commit()

async def create_game(_chat_id):
    _key = await create_key()
    async with async_session() as session:
        session.add(Game(
            key = _key,
            map_size = 0,
            status = 'created'
        ))
        session.add(Player(
            key = _key,
            chat_id = _chat_id,
            admin = True
        ))
        session.add(Match(
            chat_id = _chat_id,
            key = _key
        ))
        await session.commit()
    return _key

async def create_key():
    async with async_session() as session:
        while True:
            _key = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
            game = await session.scalar(select(Game).where(Game.key == _key))
            
            if not game:
                break

        return _key

async def update_game(_key, _game_info):
    async with async_session() as session:
        change = (update(Game)
                  .where(Game.key == _key)
                  .values(map_id = _game_info["map"]))
        await session.execute(change)
        await session.commit()

async def set_game_status_started(_key):
    async with async_session() as session:
        change = (update(Game)
                  .where(Game.key == _key)
                  .values(status = 'started'))
        await session.execute(change)
        await session.commit()

async def player_count(_key):
    async with async_session() as session:
        players = await session.scalars(select(Player).where(Player.key == _key))

        count = 0
        for player in players:
            count += 1

        return count