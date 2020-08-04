import datetime as dt
from typing import List, Optional

import pandas as pd
from heatwave_api import configuration
from heatwave_api.archivist import HeatwaveRecordsArchivist
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

    __slots__ = ("archive",)

    def __init__(self):
        self.archive = self._load_archive()

    @staticmethod
    def _load_archive():
        archive_filepath = configuration.OUTPUT_DIR / configuration.ARCHIVE_FILENAME
        if not archive_filepath.exists():
            archivist = HeatwaveRecordsArchivist(configuration.DATA_DIR)
            archivist.generate_records(archive_filepath)
        return pd.read_parquet(archive_filepath)

    def query(
        self, from_inclusive: Optional[dt.date], to_inclusive: Optional[dt.date]
    ) -> List[HeatwaveRecord]:
        results = self.archive
        if from_inclusive is not None:
            results = results.loc[
                lambda df: df["from_inclusive"] >= from_inclusive.isoformat()
            ]
        if to_inclusive is not None:
            results = results.loc[
                lambda df: df["to_inclusive"] <= to_inclusive.isoformat()
            ]

        return [
            HeatwaveRecord(
                from_inclusive=row.from_inclusive,
                to_inclusive=row.to_inclusive,
                duration=row.duration,
                number_tropical_days=row.number_tropical_days,
                max_temperature=row.max_temperature,
            )
            for _, row in results.iterrows()
        ]
