# Logger buddy

A simple logger for fastapi.

## Features

- [x] Super easy to use
- [x] `Dev`, `Full`, `Prod` modes with sane config
- [x] Auto generate request IDs to track logging
- [x] Fastapi dependency injection
- [x] Nice colors for JSON
- [x] Fastapi dependency injection
- [ ] Loki support

## Quick start

TL;DR? Check out the quick start example in ./examples/. There are a number of other examples in ./examples/\*.js.

## Usage

First add the middleware like below.

```python
app = FastAPI()
app.add_middleware(FastLoggerMiddleware, mode=Mode.dev)

```

And thats it!

You now have a nice logger. The config above also does some more magic like creating a request ID that is persisted in the logger during the whole lifecycle of the request. You will see how to use this below.

Log more like this:

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

As you can see everything passed after the first logger argument is printed in the extras section. You can use this section for debugging info.
