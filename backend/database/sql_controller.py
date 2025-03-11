from typing import Any
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload, joinedload
from database.model.models import AccessLog, User
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

    async def get_user_and_most_recent_session(
        self, email: str
    ) -> tuple[User, AccessLog]:
        user_query = await self.db.execute(
            select(User)
            .filter(User.Email == email)
            .options(selectinload(User.access_logs))
        )

        user = user_query.scalar_one_or_none()

        if user is None:
            return None, None

        latest_log = max(user.access_logs, key=lambda log: log.SignInTime, default=None)

        return user, latest_log

    async def find_all_sessions(self) -> list[AccessLog]:
        async with self.db.begin():
            results = await self.db.execute(
                select(AccessLog).options(joinedload(AccessLog.user))
            )

            return results.scalars().all()

    async def insert_session(self, session_attempt: AccessLog) -> None:
        await self.create_record(session_attempt)

    async def insert_user(self, user: User) -> None:
        user_record, session = await self.get_user_and_most_recent_session(user.Email)

        if user_record:
            return

        await self.create_record(user)
