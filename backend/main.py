from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.login import login_router
import uvicorn


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(login_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8001)
