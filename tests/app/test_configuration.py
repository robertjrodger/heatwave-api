import importlib

import pytest
from heatwave_api import configuration

pytestmark = pytest.mark.usefixtures("clean_env")

from starlette import config


def _load_with_environment(**kwargs):
    """Reset the settings module, with a given environment.

    This helps with testing that the variables from the environment take
    precedence over the variables in starlette.config via
    heatwave_api.configuration.
    """
    config.environ = config.Environ()
    for key, value in kwargs.items():
        config.environ[key] = value
    importlib.reload(configuration)


def test_api_key_from_environment():
    _load_with_environment(VM_API_KEYS="expected_key")
    assert tuple(configuration.KEYS) == ("expected_key",)


def test_api_key_supports_multiple_keys():
    _load_with_environment(VM_API_KEYS="key1,key2")
    assert frozenset(configuration.KEYS) == frozenset(("key1", "key2"))


def test_debug_mode_off_by_default():
    _load_with_environment()
    assert not configuration.DEBUG


def test_debug_mode_from_environment():
    _load_with_environment(VM_API_DEBUG="true")
    assert configuration.DEBUG
    _load_with_environment(VM_API_DEBUG="false")
    assert not configuration.DEBUG
