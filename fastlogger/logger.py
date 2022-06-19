import logging
import uuid
from fastapi import FastAPI, Request
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from fastlogger.utils import pretty_print_for_dev
import enum

# creating enumerations using class
class Mode(enum.Enum):
    tiny = "tiny"
    dev = "dev"
    prod = "prod"


logger = structlog.get_logger()


def FastLogger():
    return logger


class FastLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, mode: Mode):
        super().__init__(app)
        self.mode = mode

        structlog.configure(
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
            logger_factory=structlog.BytesLoggerFactory(),
            processors=[
                structlog.threadlocal.merge_threadlocal,
                structlog.processors.add_log_level,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                # TODO: change depending on mode
                pretty_print_for_dev,
            ],
        )
        logger.info("Fastapi logger initialized.")

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        structlog.threadlocal.clear_threadlocal()
        structlog.threadlocal.bind_threadlocal(
            url=request.url.__str__(),
            method=request.method,
            request_id=request_id,
        )

        # process the request and get the response
        response = await call_next(request)
        response.headers["request_id"] = request_id

        # Send data to loki or other indexer
        logger.info(f"{request.url.__str__()} sent to loki")

        return response
