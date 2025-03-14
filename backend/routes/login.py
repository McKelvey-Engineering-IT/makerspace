from typing import Any, Dict
from fastapi import APIRouter, Body, Depends
from database.response_builder import ResponseBuilder
from database.model.models import AccessLog, LoginRequest, User
from database.sql_controller import SQLController
from routes.dependencies import (
    get_state_manager,
    get_badgr_connector,
    get_db,
)
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from datetime import datetime, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import time

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


@login_router.get("/historical")
async def historical_lookup(
    timeFilter: str,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    TIME_FRAMES = {
        "day": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=30),
    }

    if timeFilter not in TIME_FRAMES:
        raise ValueError("Invalid timeframe. Choose 'day', 'week', or 'month'.")

    now = int(time.time() * 1000)
    time_delta = TIME_FRAMES[timeFilter]
    start_time = now - (time_delta.total_seconds() * 1000)

    query_results, last_result_id = await sql_controller.find_sessions_by_timestamp(start_time)

    return {
        "data": [ResponseBuilder.UserBasics(log.user, log) for log in query_results],
        "last_record": last_result_id,
    }


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

    user, log = await sql_controller.get_user_and_most_recent_session(
        login_request.Email
    )
    state.logins.append(ResponseBuilder.UserBasics(user, log))

    await state.flag_new_message()

    return access_payload


@login_router.post("/check_logins")
async def login_stream(
    payload = Body(...),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:

    sql_controller = SQLController(db)
    results, last_result_id = await sql_controller.find_sessions_by_id(
        payload['start_id']
    )

    return {
        "data": [ResponseBuilder.UserBasics(log.user, log) for log in results],
        "last_record": last_result_id,
    }
