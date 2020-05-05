from pathlib import Path

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config()

DEBUG = config("VM_API_DEBUG", cast=bool, default=False)
KEYS = config("VM_API_KEYS", cast=CommaSeparatedStrings, default=[])
OUTPUT_DIR = config(
    "VM_OUTPUT_DIR",
    cast=Path,
    default=Path(__file__).resolve().parent.parent.parent / "output",
)
ARCHIVE_FILENAME = "archive.parquet"
