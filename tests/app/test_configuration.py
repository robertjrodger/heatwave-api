import importlib
import os

from starlette import config
from heatwave_api import configuration


def setup_module(module):
    # Save the existing configuration environment so we can restore it later.
    module._os_environment = dict(os.environ)
    module._starlette_environment = config.environ
    os.environ.clear()


def teardown_module(module):
    # Restore the environment that was  in place before we started and re-initialize the settings.
    for key, value in module._os_environment.items():
        os.environ[key] = value
    config.environ = module._starlette_environment
    del module._os_environment
    del module._starlette_environment
    importlib.reload(configuration)


def _load_with_environment(**kwargs):
    """Reset the settings module, with a given environment."""
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
