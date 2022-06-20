# Logger buddy

A simple logger for fastapi.

## Quick start

TL;DR? Check out the quick start example in ./examples/. There are a number of other examples in ./examples/\*.js.

## Usage

```python
app = FastAPI()
app.add_middleware(FastLoggerMiddleware, mode=Mode.dev)

```

And thats it!
You now have a nice logger. Log more like this:

```python
@app.get("/")
async def root(logger=Depends(FastLogger)):

    logger.info("Hello World info")
    logger.info({"message": "json as main log"})
    logger.debug("Debuuuug", foo="foo", bar="bar")
    logger.error("Erroooor!!!", obj={"foo": "bar"}, test=test)

    return {"message": "Hello World"}


```

This produces the following in dev mode:

```bash
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Hello World info
INFO:     {'message': 'json as main log'}
DEBUG:    Debuuuug        {"bar": "bar", "foo": "foo"}
ERROR:    Erroooor!!!        {"obj": {"foo": "bar"}, "test": "test"}
INFO:     127.0.0.1:51995 - "GET / HTTP/1.1" 200 OK
```
