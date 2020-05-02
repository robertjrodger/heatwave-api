from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

__all__ = "app"

app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"
