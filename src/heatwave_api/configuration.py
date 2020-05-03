from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config()

KEYS = config("VM_API_KEYS", cast=CommaSeparatedStrings, default=[])
