import datetime as dt
from typing import List, Optional

import pandas as pd
from heatwave_api import configuration
from pydantic import BaseModel, Field


class HeatwaveRecord(BaseModel):
    from_inclusive: dt.date = Field(None, description="Start date of the heatwave.")
    to_inclusive: dt.date = Field(
        None, description="End date of the heatwave, inclusive."
    )
    duration: int = Field(None, ge=5, description="Duration of the heatwave, in days.")
    number_tropical_days: int = Field(
        None, ge=3, description="Number of days above 30 degrees during the heatwave."
    )
    max_temperature: float = Field(
        None, ge=30.0, description="Maximum temperature during the heatwave."
    )


class HeatwaveRecordsArchive:
    def __init__(self):
        self.archive = self._load_archive()

    @staticmethod
    def _load_archive():
        return pd.read_parquet(
            configuration.OUTPUT_DIR / configuration.ARCHIVE_FILENAME
        )

    def query(
        self, from_inclusive: Optional[dt.date], to_inclusive: Optional[dt.date]
    ) -> List[HeatwaveRecord]:
        results = self.archive
        if from_inclusive is not None:
            results = results.loc[
                lambda df: df["start_date"] >= from_inclusive.isoformat()
            ]
        if to_inclusive is not None:
            results = results.loc[lambda df: df["end_date"] <= to_inclusive.isoformat()]

        return [
            HeatwaveRecord(
                from_inclusive=row.start_date,
                to_inclusive=row.end_date,
                duration=row.duration,
                number_tropical_days=row.num_tropical,
                max_temperature=row.max_temp,
            )
            for _, row in results.iterrows()
        ]
