from sqlalchemy import NullPool
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

USERNAME = "jubelmakerspace@wustl.edu"
KEY = "SpartanCanvas138"
DATABASE_URL = "mysql+aiomysql://newuser:@127.0.0.1/test_database"

state_manager = StateManager()
badgr_connector = BadgrConnector(USERNAME, KEY)
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_state_manager():
    return state_manager


def get_badgr_connector():
    return badgr_connector


def get_settings():
    return Settings()
