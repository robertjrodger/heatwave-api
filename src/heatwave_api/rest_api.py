from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

__all__ = "app"

app = FastAPI()


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    """
    Check the presence of the service.
    """
    return "pong"
