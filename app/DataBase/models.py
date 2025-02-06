from typing import Optional
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(40))
    icon_id: Mapped[int] = mapped_column()
    icons_access: Mapped[int] = mapped_column()

class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(3))
    map_id: Mapped[Optional[int]] = mapped_column()
    map_size: Mapped[Optional[int]] = mapped_column()
    status: Mapped[str] = mapped_column(String(10))
    sample_message_id: Mapped[Optional[str]] = mapped_column(String(20))

class Player(Base):
    __tablename__ = 'games_players'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(3))
    chat_id = mapped_column(BigInteger)
    admin: Mapped[bool] = mapped_column()
    in_lobby: Mapped[bool] = mapped_column()
    main_message_id: Mapped[Optional[str]] = mapped_column(String(20))

class Addon(Base):
    __tablename__ = 'games_addons'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(3))
    addon_type: Mapped[str] = mapped_column(String(15))
    toggled: Mapped[bool] = mapped_column()

class Match(Base):
    __tablename__ = 'users_matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)
    key: Mapped[str] = mapped_column(String(3))
    

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)