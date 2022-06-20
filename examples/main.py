from fastapi import Depends, FastAPI
from fastlogger.logger import FastLoggerMiddleware, FastLogger, Mode

# Run with: uvicorn examples.main:dev --reload
# Used to demonstrate the usage of the middleware in dev mode.

dev = FastAPI()
dev.add_middleware(FastLoggerMiddleware, mode=Mode.dev)


@dev.get("/")
async def root(logger=Depends(FastLogger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")

    return {"message": "Hello World"}


# Run with: uvicorn examples.main:full --reload
# Used to demonstrate the usage of the middleware in full mode.

full = FastAPI()
full.add_middleware(FastLoggerMiddleware, mode=Mode.full)


@full.get("/")
async def root(logger=Depends(FastLogger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")

    return {"message": "Hello World"}
