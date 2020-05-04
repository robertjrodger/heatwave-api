from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

config = Config()

DEBUG = config("VM_API_DEBUG", cast=bool, default=False)
KEYS = config("VM_API_KEYS", cast=CommaSeparatedStrings, default=[])
