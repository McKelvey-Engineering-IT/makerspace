from sqlalchemy import NullPool
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()
state_manager = StateManager()
badgr_connector = BadgrConnector(settings.BADGR_MAKERSPACE_EMAIL, settings.BADGR_MAKERSPACE_PASSWORD)
engine = create_async_engine(settings.DB_CONNECTION_STRING, poolclass=NullPool)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_settings() -> Settings:
    return settings

async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_state_manager():
    return state_manager


def get_badgr_connector():
    return badgr_connector
