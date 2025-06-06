import os, logging, uvicorn
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from config import Settings
from routes.login import login_router

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

settings = Settings()

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

    @app.get("/sign_in", response_class=HTMLResponse)
    async def catch_all():
        index_path = os.path.join(settings.FRONTEND_BUILD_DIR, "index.html")

        if not os.path.exists(index_path):
            return JSONResponse(status_code=404, content={"detail": "Frontend index.html not found."})
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())

    public_dir = os.path.join(settings.FRONTEND_BUILD_DIR, "public")
    if os.path.exists(public_dir):
        app.mount("/public", StaticFiles(directory=public_dir), name="public")

    frontend_static_dir = os.path.join(settings.FRONTEND_BUILD_DIR, "static")
    if os.path.exists(frontend_static_dir):
        app.mount("/static", StaticFiles(directory=frontend_static_dir), name="static")

    if os.path.exists(settings.FRONTEND_BUILD_DIR):
        app.mount("/", StaticFiles(directory=settings.FRONTEND_BUILD_DIR, html=True), name="frontend")

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error on {request.url}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error. Please contact support."},
        )

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)
