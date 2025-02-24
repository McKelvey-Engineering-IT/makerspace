import asyncio
from typing import Any, AsyncGenerator, Dict
from fastapi import APIRouter, Request, Depends
from sse_starlette import EventSourceResponse
from routes.dependencies import get_state_manager, get_settings
from controllers.state_manager import StateManager
from config import Settings

login_router = APIRouter(prefix="/logins", tags=["Logins"])


@login_router.get("/login")
async def user_login(
    username: str, state: StateManager = Depends(get_state_manager)
) -> Dict[str, Any]:

    payload = {
        "id": "item",
        "name": username,
        "studentId": f"{username}@wustl.edu",
        "signInTime": "Today",
        "isMember": False,
    }

    state.flag_new_message()

    return payload


@login_router.get("/check_logins")
async def login_stream(request: Request) -> EventSourceResponse:
    async def event_generator(
        config: Settings = Depends(get_settings),
        state: StateManager = Depends(get_state_manager),
    ) -> AsyncGenerator[str, None]:
        while True:
            if await request.is_disconnected():
                break

            await asyncio.sleep(config.MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())
