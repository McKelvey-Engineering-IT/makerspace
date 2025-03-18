import os, urllib.parse
from sqlalchemy import NullPool
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

encoded_password = urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))
DATABASE_URL = f"mssql+aioodbc://{os.getenv('DB_USER')}:{encoded_password}@{os.getenv('DB_SERVER')}/{os.getenv('DB')}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes"

state_manager = StateManager()
badgr_connector = BadgrConnector({os.getenv('MAKERSPACE_EMAIL')}, {os.getenv('MAKERSPACE_PASSWORD')})
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_state_manager():
    return state_manager


def get_badgr_connector():
    return badgr_connector


def get_settings():
    return Settings()
