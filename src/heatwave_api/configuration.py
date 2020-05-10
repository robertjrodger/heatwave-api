from pathlib import Path

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

repo_root_dir = Path(__file__).resolve().parent.parent.parent
config = Config()

DEBUG = config("VM_API_DEBUG", cast=bool, default=False)
KEYS = config("VM_API_KEYS", cast=CommaSeparatedStrings, default=[])
DATA_DIR = config("VM_DATA_DIR", cast=Path, default=repo_root_dir / "data")
OUTPUT_DIR = config("VM_OUTPUT_DIR", cast=Path, default=repo_root_dir / "output")
ARCHIVE_FILENAME = "archive.parquet"
