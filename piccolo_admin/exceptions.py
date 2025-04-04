import logging

from starlette.middleware.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def handle_auth_exception(request: Request, exc: Exception):
    return JSONResponse({"error": "Auth failed"}, status_code=401)


async def log_error(request: Request, exc: HTTPException):
    logger.exception("Server error")
    raise exc
