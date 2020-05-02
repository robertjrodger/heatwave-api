from fastapi import FastAPI

__all__ = "app"

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "pong"}
