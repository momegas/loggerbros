from fastapi import Depends, FastAPI
from fastlogger.logger import FastLoggerMiddleware, FastLogger, Mode


app = FastAPI()
app.add_middleware(FastLoggerMiddleware, mode=Mode.dev)


@app.get("/")
async def root(logger=Depends(FastLogger)):

    logger.info("Hello World info")
    logger.info({"message": "testing json as first arg"})
    logger.debug("Debuuuug", charis="is beautiful", megas="malaka")

    logger.error(
        "Erroooor!!!", extra={"foo": "bar"}, charis="is beautiful", megas="malaka"
    )

    return {"message": "Hello World"}
