import logging
import uuid
from fastapi import FastAPI, Request
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from fastlogger.utils import pretty_print_for_dev, pretty_print_json
import enum

# creating enumerations using class
class Mode(enum.Enum):
    dev = "dev"
    full = "full"
    prod = "prod"


logger = structlog.get_logger()


def FastLogger():
    return logger


class FastLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, mode: Mode):
        super().__init__(app)
        self.mode = mode

        # Get config according to mode
        print_fn = self.get_print_fn()
        min_log_level = self.get_min_log_level()

        structlog.configure(
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(min_log_level),
            logger_factory=structlog.BytesLoggerFactory(),
            processors=[
                structlog.threadlocal.merge_threadlocal,
                structlog.processors.add_log_level,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                print_fn,
            ],
        )
        logger.info("Fastapi logger initialized.")

    async def dispatch(self, request: Request, call_next):
        """
        Used by FastAPI as middleware.
        It creates a request id and adds it to the log as well as the url and method.
        """

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
        # logger.info(f"{request.url.__str__()} sent to loki")

        return response

    def get_print_fn(self):
        """Return the print function. Default is printing for dev mode."""

        if self.mode == Mode.dev:
            return pretty_print_for_dev
        elif self.mode == Mode.full:
            return pretty_print_json
        # elif self.mode == Mode.prod:
        #     return pretty_print_for_prod
        else:
            return pretty_print_for_dev

    def get_min_log_level(self):
        """Return the minimum log level. Default is logging.DEBUG."""

        if self.mode == Mode.dev:
            return logging.DEBUG
        elif self.mode == Mode.prod:
            return logging.INFO
        else:
            return logging.INFO
