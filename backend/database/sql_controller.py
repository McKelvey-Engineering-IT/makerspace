from typing import Any, Dict, Optional

from sqlalchemy import select, text
from database.model.models import AccessLog, AccessLogResponse, User, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


class SQLController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_record(self, record: Any) -> None:
        self.db.add(record)
        
        await self.db.commit()

    async def _find_records_by_text(self, query: str) -> list:
        result = await self.db.execute(text(query))

        return [dict(row) for row in result.fetchall()]

    async def find_user_record_by_email(self, email: str) -> Optional[User]:
        async with self.db.begin():
            results = await self.db.execute(select(User).filter(User.Email == email))

            response = results.scalar_one_or_none()

            if not response:
                return None

            return UserResponse.model_validate(response).model_dump()

    async def find_all_sessions(self) -> list:
        async with self.db.begin():
            results = await self.db.execute(select(AccessLog))
            users = results.scalars().all()

            return [
                AccessLogResponse.model_validate(user).model_dump() for user in users
            ]

    async def insert_session(self, session_attempt: AccessLog) -> None:
        await self.create_record(session_attempt)

    async def insert_user(self, user: User) -> None:
        user_record = await self.find_user_record_by_email(user.Email)

        if user_record:
            return

        await self.create_record(user)
