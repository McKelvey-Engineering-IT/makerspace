from typing import Any, Optional, Union
from sqlalchemy import insert, select, text, update
from sqlalchemy.orm import selectinload, joinedload
from database.model.models import AccessLog, BadgeSnapshot, User, EmailException
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

    async def insert_session(self, session_attempt: AccessLog) -> int:
        await self.create_record(session_attempt)

        return session_attempt.ID

    async def find_sessions_by_timestamp(
        self, start_time
    ) -> tuple[list[AccessLog], int]:
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
                .filter(AccessLog.ID > starting_id)
            )

            result = results.scalars().all()
            lastEntry = result[-1].ID if result else starting_id

            return result, lastEntry

    async def find_session_by_id(self, log_id: int) -> AccessLog:
        async with self.db.begin():
            result = await self.db.execute(
                select(AccessLog)
                .options(
                    joinedload(AccessLog.user),
                    joinedload(AccessLog.badge_snapshot)
                )
                .filter(AccessLog.ID == log_id)
                .distinct()
            )
            
            return result.unique().scalar_one_or_none()

    async def insert_user(self, user: User) -> None:
        user_record, session = await self.get_user_and_most_recent_session(user.Email)

        if user_record:
            return

        await self.create_record(user)

    async def badge_snapshot_insert(self, records: list[BadgeSnapshot]) -> None:
        async with self.db.begin():
            self.db.add_all(records)
            
            await self.db.commit()

    async def find_email_exception(self, email: str) -> Optional[str]:
        async with self.db.begin():
            result = await self.db.execute(
                select(EmailException.badgr_email)
                .filter(EmailException.exception_email == email)
            )
            return result.scalar_one_or_none()

    async def get_user(self, email: str):
        result = await self.db.execute(
            select(User).where(User.Email == email)
        )
        return result.scalar_one_or_none()

    async def update_user(self, email: str, **fields):
        if not fields:
            return
        stmt = (
            update(User)
            .where(User.Email == email)
            .values(**fields)
        )
        await self.db.execute(stmt)
        await self.db.commit()
