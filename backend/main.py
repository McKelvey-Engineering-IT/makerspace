import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

    frontend_build_dir = os.path.join(os.getenv("APP_HOME", "/app"), "frontend", "build")
    
    app.mount("/", StaticFiles(directory=frontend_build_dir, html=True), name="static")
    
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=32777)