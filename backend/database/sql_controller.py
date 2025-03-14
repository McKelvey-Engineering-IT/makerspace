from typing import Any, Union
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload, joinedload
from database.model.models import AccessLog, User
from sqlalchemy.ext.asyncio import AsyncSession


class SQLController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_record(self, record: Union[User, AccessLog]) -> None:
        self.db.add(record)

        await self.db.commit()

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

    async def find_most_recent_sessions(self) -> list[AccessLog]:
        async with self.db.begin():
            results = await self.db.execute(
                select(AccessLog)
                .options(joinedload(AccessLog.user))
                .order_by(AccessLog.SignInTime.desc())
                .limit(20)
            )

            return results.scalars().all()

    async def insert_session(self, session_attempt: AccessLog) -> None:
        await self.create_record(session_attempt)

    async def find_sessions_by_timestamp(self, start_time) -> tuple[list[AccessLog], int]:
        async with self.db.begin():
            results = await self.db.execute(
                select(AccessLog)
                .options(joinedload(AccessLog.user))
                .filter(AccessLog.SignInTime >= start_time)
            )

            result = results.scalars().all()
            lastEntry = result[-1].ID if result else None

            return result, lastEntry

    async def find_sessions_by_id(self, starting_id) -> tuple[list[AccessLog], int]:
        async with self.db.begin():
            results = await self.db.execute(
                select(AccessLog)
                .options(joinedload(AccessLog.user))
                .filter(AccessLog.ID >= starting_id)
            )
        
            result = results.scalars().all()
            lastEntry = result[-1].ID if result else None

            return result, lastEntry

    async def insert_user(self, user: User) -> None:
        user_record, session = await self.get_user_and_most_recent_session(user.Email)

        if user_record:
            return

        await self.create_record(user)
