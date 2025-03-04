import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from fastapi import APIRouter, Request, Depends
from sse_starlette import EventSourceResponse
from controllers.db_base import DBBase
from routes.dependencies import get_state_manager, get_settings, get_database
from controllers.state_manager import StateManager
from config import Settings

login_router = APIRouter(prefix="/logins", tags=["Logins"])


@login_router.get("/logout")
async def user_logout(
    username: str, state: StateManager = Depends(get_state_manager), db: DBBase = Depends(get_database)
) -> str:
    username = f"{username}@wustl.edu"

    record = db.find_record(username)
    record.update({"activeSession": False})

    db.update_record(username, record)

    return "Record update complete"


@login_router.get("/login")
async def user_login(
    username: str,
    state: StateManager = Depends(get_state_manager),
    db: DBBase = Depends(get_database),
) -> Dict[str, Any]:

    payload = {
        "id": "item",
        "name": username,
        "email": f"{username}@wustl.edu",
        "signInTime": "Today",
        "isMember": False,
        "activeSession": True,
    }

    await db.insert_session(payload)
    await state.flag_new_message()

    return payload


@login_router.get("/check_logins")
async def login_stream(
    request: Request,
    config: Settings = Depends(get_settings),
    db: DBBase = Depends(get_database),
) -> EventSourceResponse:
    async def event_generator() -> AsyncGenerator[str, None]:
        while True:
            if await request.is_disconnected():
                break

            payload = {"data": db.find_all_active_sessions()}

            yield f"{json.dumps(payload)}"

            await asyncio.sleep(config.MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())
