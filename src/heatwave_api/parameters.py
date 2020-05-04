import datetime as dt

from fastapi.exceptions import HTTPException
from fastapi.requests import Request


def date_parameter(request: Request, name: str) -> dt.date:
    if name not in request.query_params:
        raise HTTPException(
            status_code=400, detail=f"Missing '{name}' query parameter."
        )
    try:
        value = dt.date.fromisoformat(request.query_params[name])
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid '{name}' parameter; must be in the format YYYY-MM-DD.",
        )

    return value
