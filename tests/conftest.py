import importlib
import os

import pytest
from heatwave_api import configuration
from starlette import config


@pytest.fixture
def clean_env():
    # Save the existing configuration environment so we can restore it later.
    os_environment = dict(os.environ)
    starlette_environment = config.environ
    os.environ.clear()
    yield
    # Restore the environment that was in place before we started and re-initialize the settings.
    for key, value in os_environment.items():
        os.environ[key] = value
    config.environ = starlette_environment
    del os_environment
    del starlette_environment
    importlib.reload(configuration)
