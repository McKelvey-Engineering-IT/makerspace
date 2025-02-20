import asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn


CURRENT_LOGINS = []
MESSAGE_STREAM_DELAY = 5  
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  
login_event = asyncio.Event()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


def new_logins():
    if len(CURRENT_LOGINS) > 0:
        return True

@app.get('/login')
async def user_login(username: str):
    CURRENT_LOGINS.append(username)
    login_event.set()
    login_event.clear()
    
    return "success"

@app.get('/check_logins')
async def login_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            print("checking")
            if new_logins():
                print("sending")
                yield f"event: new_login\n" \
                      f"data: test\n" \
                      f"message: test\n" \
                      f"retry: 15000\n\n"

            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)