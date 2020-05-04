import importlib
from types import ModuleType
from typing import Sequence

from starlette import config

from heatwave_api import configuration


def _load_settings(extra_reload_modules: Sequence[ModuleType] = (), **kwargs):
    """Reset the configuration environment used for settings."""
    config.environ = config.Environ()
    for key, value in kwargs.items():
        config.environ[key] = value
    importlib.reload(configuration)
    for module in extra_reload_modules:
        importlib.reload(module)
