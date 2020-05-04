import datetime as dt
from typing import List

from fastapi import FastAPI, status, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from heatwave_api import configuration
from heatwave_api.archive import HeatwaveRecordsArchive, HeatwaveRecord
from heatwave_api.authentication import TrustedKeyMiddleware

__all__ = "app"

archive = HeatwaveRecordsArchive()

app = FastAPI()
app.add_middleware(TrustedKeyMiddleware, allowed_keys=configuration.KEYS)


@app.get("/ping", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def ping():
    """
    Check the presence of the service.
    """
    return "pong"


@app.get(
    "/records", status_code=status.HTTP_200_OK, response_model=List[HeatwaveRecord]
)
async def records(
    from_inclusive: dt.date = Query(None, example="2020-04-23"),
    to_inclusive: dt.date = Query(None, example="2020-04-25"),
):
    # TODO: Document the additional 400 response? https://fastapi.tiangolo.com/advanced/additional-responses/
    """
    Get records
    """
    if from_inclusive and to_inclusive and from_inclusive >= to_inclusive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value of from_inclusive must be less than that of to_inclusive.",
        )
    heatwave_records = archive.query(from_inclusive, to_inclusive)

    return heatwave_records
