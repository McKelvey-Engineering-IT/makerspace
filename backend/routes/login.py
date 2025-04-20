from typing import Any, Dict
from fastapi import APIRouter, Body, Depends
from config import Settings
from database.response_builder import ResponseBuilder
from database.model.models import AccessLog, BadgeSnapshot, LoginRequest, User
from database.sql_controller import SQLController
from routes.dependencies import (
    get_state_manager,
    get_badgr_connector,
    get_db,
    get_settings
)
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from datetime import datetime, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.badgr_session import BadgrSession
import time
from controllers.user_controller import UserController

login_router = APIRouter(prefix="/logins", tags=["Logins"])


@login_router.get("/retrieve_user")
async def user_badges(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    
    session = await sql_controller.find_session_by_id(log_id)
    if not session:
        return {"error": "Session not found"}
    
    badge_data = BadgrSession.format_badges(
        [{
            "ID": badge.ID,
            "Narrative_Detail": badge.Narrative_Detail,
            "Narrative_Title": badge.Narrative_Title,
            "IssuedOn": badge.IssuedOn,
            "CreatedAt": badge.CreatedAt,
            "Revoked": badge.Revoked,
            "Revocation_Reason": badge.Revocation_Reason,
            "BadgeClass": badge.BadgeClass,
            "ImageURL": badge.ImageURL,
            "AccessLogID": badge.AccessLogID
        } for badge in session.badge_snapshot],
        settings.BADGR_MAKERSPACE_MEMBER_BADGR
    )
    
    return {**badge_data, **ResponseBuilder.UserBasics(session.user, session)}


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
        "full": timedelta(days=365 * 5),
        "30min": timedelta(minutes=30),
        "2hr": timedelta(hours=2),
    }

    if timeFilter not in TIME_FRAMES:
        raise ValueError("Invalid timeframe. Choose 'day', 'week', or 'month'.")

    now = int(time.time() * 1000)
    time_delta = TIME_FRAMES[timeFilter]
    start_time = now - (time_delta.total_seconds() * 1000)

    query_results, last_result_id = await sql_controller.find_sessions_by_timestamp(
        start_time
    )

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
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    sql_controller = SQLController(db)
    
    badgr_email = await sql_controller.find_email_exception(login_request.Email)
    lookup_email = badgr_email or login_request.Email
    
    badgr_session = BadgrSession(lookup_email, badgr_connect, settings.BADGR_MAKERSPACE_MEMBER_BADGR)
    
    access_payload = {
        "Email": login_request.Email,
        "SignInTime": datetime.now().timestamp() * 1000,
        "SignInTimeExternal": login_request.SignInTime,
        "membershipYears": badgr_session.membership_years,
        "IsMember": badgr_session.member_status,
        "School": getattr(login_request, "School", None),
        "ClassLevel": getattr(login_request, "ClassLevel", None),
    }

    user_payload = {
        "Email": login_request.Email,
        "FirstName": login_request.FirstName,
        "LastName": login_request.LastName,
        "StudentID": login_request.StudentID,
    }

    await sql_controller.insert_user(User(**user_payload))

    session_id = await sql_controller.insert_session(AccessLog(**access_payload))
    badges = badgr_session.get_user_badges(session_id)

    total_badges = [
        badge 
        for level in badges["badges"] 
        for badge in level["badges"]
    ]
    
    badgr_snapshot = [BadgeSnapshot(**badge) for badge in total_badges]

    await sql_controller.badge_snapshot_insert(badgr_snapshot)

    user, log = await sql_controller.get_user_and_most_recent_session(
        login_request.Email
    )
    state.logins.append(ResponseBuilder.UserBasics(user, log))

    await state.flag_new_message()

    return access_payload


@login_router.post("/check_logins")
async def login_stream(
    payload=Body(...),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:

    sql_controller = SQLController(db)
    results, last_result_id = await sql_controller.find_sessions_by_id(
        payload["start_id"]
    )

    return {
        "data": [ResponseBuilder.UserBasics(log.user, log) for log in results],
        "last_record": last_result_id,
    }
