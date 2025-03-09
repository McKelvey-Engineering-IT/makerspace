import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from fastapi import APIRouter, Body, Request, Depends
from sse_starlette import EventSourceResponse
from controllers.db_base import DBBase
from routes.dependencies import (
    get_state_manager,
    get_settings,
    get_database,
    get_badgr_connector,
)
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from datetime import datetime
import time

login_router = APIRouter(prefix="/logins", tags=["Logins"])


@login_router.get("/logout")
async def user_logout(
    email: str,
    state: StateManager = Depends(get_state_manager),
    db: DBBase = Depends(get_database),
) -> str:
    email = f"{email}@wustl.edu"

    record = db.find_record(email)
    record.update({"activeSession": False})

    db.update_record(email, record)

    return "Record update complete"


@login_router.get("/retrieve_user")
async def user_badges(
    email: str,
    badgr_connect: BadgrConnector = Depends(get_badgr_connector),
    db: DBBase = Depends(get_database),
) -> Dict[str, Any]:
    user = badgr_connect.get_user(email)
    user_session = db.find_record(email)

    if user["name"].lower() == "unregistered":
        user["name"] = user_session["name"]

    return {**user, "lastSignIn": user_session["signInTime"]}


@login_router.post("/login")
async def user_login(
    Email: str = Body(...),
    FirstName: str = Body(...),
    LastName: str = Body(...),
    SignInTime: str = Body(...),
    StudentID: str = Body(...),
    state: StateManager = Depends(get_state_manager),
    db: DBBase = Depends(get_database),
    badgr_connect: BadgrConnector = Depends(get_badgr_connector),
) -> Dict[str, Any]:
    user = badgr_connect.get_user(Email)
    combined_name = f"{FirstName} {LastName}"

    if user["name"].lower() == "unregistered":
        user["name"] = combined_name

    payload = {
        "id": StudentID,
        "name": user["name"],
        "email": Email,
        "signInTime": datetime.now().timestamp() * 1000,
        "isMember": user["isMember"],
        "activeSession": True,
    }

    db.insert_session(payload)

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
