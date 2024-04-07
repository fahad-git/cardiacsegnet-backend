from typing import List
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse
from core.exceptions import CustomException
from core.database.dbClient import MongoDBClient
from core.fastapi.middlewares import AuthenticationMiddleware, AuthBackend, ResponseLoggerMiddleware
from api import router
from core.database.session import set_session_context, get_session_context
from core.config import config

# Defining Error Handlers and Middlewares
def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)
    

def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=[config.ALLOWED_ORIGIN_DEVELOPMENT, config.ALLOWED_ORIGIN_BETA, config.ALLOWED_ORIGIN_PROD, config.ALLOWED_ORIGIN_PROD_SEC],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["Content-Type", "*"],
            
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(ResponseLoggerMiddleware),
    ]
    return middleware

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Medical Image Analytics",
        description="This is base for medical image analytics project developed by @fahad",
        version="1.0.0",
        docs_url=None if config.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if config.ENVIRONMENT == "production" else "/redoc",
        # dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_

app = create_app()

@app.on_event("startup")
def startup_db_client():
    # Example usage:
    print("Connecting database...")
    db_client = MongoDBClient(config.MONGODB_URL_LOCAL, "ACSP")
    db_client.open_connection()
    print("Databases connection established.")
    print("Storing database connection to session.")
    set_session_context(db_client)
    print("Sessiont saved.")

@app.on_event("shutdown")
def shutdown_db_client():
    db_client = get_session_context()
    db_client.close_connection()