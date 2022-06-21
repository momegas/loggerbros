from fastapi import Depends, FastAPI
from loggerbros.logger import LoggerbrosMiddleware, Logger, Mode

# Run with: uvicorn examples.main:dev --reload
# Used to demonstrate the usage of the middleware in dev mode.

app = FastAPI()
app.add_middleware(LoggerbrosMiddleware, mode=Mode.dev)


@app.get("/")
async def dev_handler(logger=Depends(Logger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")

    return {"message": "Hello World"}
