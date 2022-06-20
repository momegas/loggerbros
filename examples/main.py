from fastapi import Depends, FastAPI
from fastlogger.logger import FastLoggerMiddleware, FastLogger, Mode


app = FastAPI()
app.add_middleware(FastLoggerMiddleware, mode=Mode.dev)


@app.get("/")
async def root(logger=Depends(FastLogger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")

    return {"message": "Hello World"}
