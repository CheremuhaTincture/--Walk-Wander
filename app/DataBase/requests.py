from app.DataBase.models import async_session
from app.DataBase.models import User, Game, Player, Match
from sqlalchemy import select, update, delete
from random import randint

#Управление пользователем
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
            icon_id = randint(0, 1),
            icons_access = 1
        ))
        await session.commit()

async def change_nick(_chat_id, new_name):
    async with async_session() as session:
        change = (update(User)
                  .where(User.chat_id == _chat_id)
                  .values(name = new_name))
        await session.execute(change)
        await session.commit()
    
async def icon_change(_chat_id, _icon_id):
    async with async_session() as session:
        change = (update(User)
                  .where(User.chat_id == _chat_id)
                  .values(icon_id = _icon_id))
        await session.execute(change)
        await session.commit()

async def erase_player(_chat_id, _key):
    async with async_session() as session:
        change = (delete(Player)
                  .where(Player.chat_id == _chat_id,
                         Player.key == _key))
        await session.execute(change)
        await session.commit()

async def join_game(_chat_id, _key):
    async with async_session() as session:
        player = await session.scalar(select(Player)
                                      .where(Player.chat_id == _chat_id,
                                             Player.key == _key))

        if not player:
            session.add(Player(
                chat_id = _chat_id,
                key = _key,
                admin = False,
                in_lobby = True
            ))
            await session.commit()




#Управление игрой
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
            admin = True,
            in_lobby = True
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



#Сбор информации
async def player_count(_key):
    async with async_session() as session:
        players = await session.scalars(select(Player).where(Player.key == _key))

        count = 0
        for player in players:
            count += 1

        return count

async def everybody_are_ready(_key):
    async with async_session() as session:
        all_players = await player_count(_key)

        players = await session.scalars(select(Player)
                                        .where(Player.key == _key,
                                               Player.in_lobby == True))

        players_in_lobby = 0
        for player in players:
            players_in_lobby += 1

        if players_in_lobby == all_players:
            return True
        else:
            return False

async def icons_get(_chat_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == _chat_id))

        return user.icons_access

async def get_my_games(_chat_id):
    async with async_session() as session:
        players = await session.scalars(select(Player).where(Player.chat_id == _chat_id))

        games = []
        for player in players:
            games.append(player.key)
        return games

async def get_game_info(_key):
    async with async_session() as session:
        game = await session.scalar(select(Game).where(Game.key == _key))

        num_of_players = await player_count(_key)

        addons = 0

        return {
            'map_id' : game.map_id,
            'map_size' : game.map_size,
            'status' : game.status,
            'num_of_players' : num_of_players,
            'addons' : addons
        }

async def game_is_created(_key):
    async with async_session() as session:
        game = await session.scalar(select(Game).where(Game.key == _key))

        if game.status == 'created':
            return True
        else:
            return False
        
async def chosen_icon(_chat_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.chat_id == _chat_id))

        return user.icon_id

async def player_is_admin(_chat_id, _key):
    async with async_session() as session:
        player = await session.scalar(select(Player).
                                      where(Player.chat_id == _chat_id,
                                            Player.key == _key))

        return player.admin