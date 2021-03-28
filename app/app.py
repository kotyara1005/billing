from asyncpg.exceptions import UniqueViolationError
from fastapi import FastAPI
from fastapi.exceptions import (
    RequestValidationError,
    StarletteHTTPException,
)

from app.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
    unique_violation_error_handler,
)
from app.models import database
from app.views import router

# TODO tests
# TODO philosofers


def create_app() -> FastAPI:
    app = FastAPI(
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
        exception_handlers={
            StarletteHTTPException: http_exception_handler,
            RequestValidationError: request_validation_exception_handler,
            UniqueViolationError: unique_violation_error_handler,
        },
    )
    app.include_router(router)

    @app.get("/ping")
    def ping():
        return {"text": "pong"}

    return app
