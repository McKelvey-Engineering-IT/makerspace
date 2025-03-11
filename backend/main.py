import os
from dotenv import load_dotenv
from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from routes.login import login_router
import uvicorn

load_dotenv()

if os.getenv("LOCALDEV"):
    frontend_build_dir = os.path.join("..", "frontend", "build")
    serving_port = 8001
else:
    frontend_build_dir = os.path.join(
        os.getenv("APP_HOME", "/app"), "frontend", "build"
    )
    serving_port = 32776


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(login_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(frontend_build_dir, "static")),
        name="static",
    )

    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def catch_all(full_path: str):
        return HTMLResponse(open(os.path.join(frontend_build_dir, "index.html")).read())

    app.mount("/", StaticFiles(directory=frontend_build_dir, html=True), name="static")

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=serving_port)
