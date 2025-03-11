import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from fastapi import APIRouter, Request, Depends
from sse_starlette import EventSourceResponse
from database.response_builder import ResponseBuilder
from database.model.models import AccessLog, LoginRequest, User
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

    badgr_data = badgr_connect.get_user_badges(email)
    user, session = await sql_controller.get_user_and_most_recent_session(email)

    return {**badgr_data, **ResponseBuilder.UserBasics(user, session)}


@login_router.post("/login")
async def user_login(
    login_request: LoginRequest,
    state: StateManager = Depends(get_state_manager),
    db: AsyncSession = Depends(get_db),
    badgr_connect: BadgrConnector = Depends(get_badgr_connector),
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    badgr_data = badgr_connect.get_user_badges(login_request.Email)

    access_payload = {
        "Email": login_request.Email,
        "SignInTime": datetime.now().timestamp() * 1000,
        "SignInTimeExternal": login_request.SignInTime,
        "IsMember": badgr_data["isMember"],
    }

    user_payload = {
        "Email": login_request.Email,
        "FirstName": login_request.FirstName,
        "LastName": login_request.LastName,
        "StudentID": login_request.StudentID,
    }

    await sql_controller.insert_user(User(**user_payload))
    await sql_controller.insert_session(AccessLog(**access_payload))
    await state.flag_new_message()

    return access_payload


@login_router.get("/check_logins")
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
            payload = {
                "data": [
                    ResponseBuilder.UserBasics(log.user, log)
                    for log in response_payload
                ]
            }

            yield f"{json.dumps(payload)}"

            await asyncio.sleep(config.MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())
