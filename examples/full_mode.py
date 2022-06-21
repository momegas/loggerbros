from fastapi import Depends, FastAPI
from loggerbros.logger import LoggerbrosMiddleware, Logger, Mode

# Run with: uvicorn examples.main:full --reload
# Used to demonstrate the usage of the middleware in full mode.


app = FastAPI()
app.add_middleware(LoggerbrosMiddleware, mode=Mode.full)


@app.get("/")
async def full_handler(logger=Depends(Logger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test="test")

    return {"message": "Hello World"}
