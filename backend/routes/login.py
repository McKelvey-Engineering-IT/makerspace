import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from fastapi import APIRouter, Body, Request, Depends
from sse_starlette import EventSourceResponse
from database.model.models import AccessLog, User, UserResponse
from database.sql_controller import SQLController
from routes.dependencies import (
    get_state_manager,
    get_settings,
    get_badgr_connector,
    get_db,
)
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

login_router = APIRouter(prefix="/logins", tags=["Logins"])


@login_router.get("/retrieve_user")
async def user_badges(
    email: str,
    badgr_connect: BadgrConnector = Depends(get_badgr_connector),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    user = badgr_connect.get_user_badges(email)
    user_session = await sql_controller.find_user_record_by_email(email)

    if user["name"].lower() == "unregistered":
        user["name"] = user_session.get("Name", "Unregistered")

    return {**user, **user_session}


@login_router.post("/login")
async def user_login(
    Email: str = Body(...),
    FirstName: str = Body(...),
    LastName: str = Body(...),
    SignInTime: str = Body(...),
    StudentID: int = Body(...),
    state: StateManager = Depends(get_state_manager),
    db: AsyncSession = Depends(get_db),
    badgr_connect: BadgrConnector = Depends(get_badgr_connector),
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    user = badgr_connect.get_user_badges(Email)
    combined_name = f"{FirstName} {LastName}"
    timestamp = datetime.now().timestamp() * 1000

    if user["name"].lower() == "unregistered":
        user["name"] = combined_name

    access_payload = {
        "StudentID": StudentID,
        "FirstName": FirstName,
        "LastName": LastName,
        "Name": combined_name,
        "Email": Email,
        "SignInTime": timestamp,
        "SignInTimeExternal": SignInTime,
        "IsMember": user["isMember"],
    }

    user_payload = {
        "FirstName": FirstName,
        "LastName": LastName,
        "Name": combined_name,
        "Email": Email,
        "LastSignIn": timestamp,
    }

    user_insertion = User(**user_payload)
    await sql_controller.insert_user(user_insertion)

    access_insertion = AccessLog(**access_payload)
    await sql_controller.insert_session(access_insertion)
    await state.flag_new_message()

    return access_payload


@login_router.get("/check_logins", response_model=UserResponse)
async def login_stream(
    request: Request,
    config: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
) -> EventSourceResponse:
    sql_controller = SQLController(db)

    async def event_generator() -> AsyncGenerator[str, None]:
        while True:
            if await request.is_disconnected():
                break

            response_payload = await sql_controller.find_all_sessions()
            payload = {"data": response_payload}

            yield f"{json.dumps(payload)}"

            await asyncio.sleep(config.MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())
