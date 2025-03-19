from routes.dependencies import get_db, get_badgr_connector
from database.sql_controller import SQLController
from database.model.models import User, AccessLog

import pandas as pd

from sqlalchemy import NullPool, create_engine
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

df = pd.read_excel("data_ingested.xlsx", sheet_name=0)
df.fillna("MISSING", inplace=True)

ingested_users = []
table1_data = []
table2_data = []

for _, row in df.iterrows():
    user_payload = {
        "Email": row["Email"],
        "FirstName": row["First Name"],
        "LastName": row["Last Name"],
        "StudentID": "MISSING",
    }

    dt_object = datetime.strptime(row["Sign in Time"], "%m/%d/%Y %I:%M:%S %p")
    unix_timestamp_ms = int(dt_object.timestamp() * 1000)

    access_payload = {
        "Email": row["Email"],
        "SignInTime": unix_timestamp_ms,
        "SignInTimeExternal": row["Sign in Time"],
        "IsMember": True,
    }

    if row["Email"] not in ingested_users:
        ingested_users.append(row["Email"])
        table1_data.append(user_payload)

    table2_data.append(access_payload)

print(f"Table 1: {len(table1_data)} records, Table 2: {len(table2_data)} records")


async def insert_data():
    async for session in get_db():
        async with session.begin():  # Ensures atomic transaction
            session.add_all([User(**data) for data in table1_data])
            session.add_all([AccessLog(**data) for data in table2_data])

        await session.commit()


import asyncio

asyncio.run(insert_data())
