import heatwave_api.rest_api
import pytest
from fastapi import status
from fastapi.testclient import TestClient

import re
from . import _load_settings

_load_settings(
    VM_API_DEBUG="true",
    VM_API_KEYS="test_key",
    extra_reload_modules=(heatwave_api.rest_api,),
)

from heatwave_api.rest_api import app  # noqa: E402

api_key_headers = {"X-API-KEY": "test_key"}


@pytest.fixture(scope="module")
def client():
    """
    Make a 'client' fixture available to test cases.
    """
    return TestClient(app)


def test_ping_available(client):
    response = client.get("/ping", headers=api_key_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "pong"


def test_ping_requires_api_key(client):
    error_response = client.get("/ping")
    # We did not supply an API key, so should have a 403 response.
    assert error_response.status_code == status.HTTP_403_FORBIDDEN


def test_records_available(client):
    response = client.get("/records", headers=api_key_headers)
    # Just check that we get a JSON payload back.
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert response.json() is not None


def test_records_requires_api_key(client):
    error_response = client.get("/records")
    # We did not supply an API key, so should have a 403 response.
    assert error_response.status_code == status.HTTP_403_FORBIDDEN


def test_records_from_inclusive_before_to_inclusive_validation(client):
    url = "/records?from_inclusive=2000-01-01&to_inclusive=2000-12-31"
    response = client.get(url, headers=api_key_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert response.json() is not None


def test_records_from_inclusive_equals_to_inclusive_validation(client):
    url = "/records?from_inclusive=2010-01-01&to_inclusive=2010-01-01"
    error_response = client.get(url, headers=api_key_headers)
    assert error_response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        b"Value of from_inclusive must be less than that of to_inclusive"
        in error_response.content
    )


def test_records_from_inclusive_after_to_inclusive_validation(client):
    url = "/records?from_inclusive=2010-12-21&to_inclusive=2010-01-01"
    error_response = client.get(url, headers=api_key_headers)
    assert error_response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        b"Value of from_inclusive must be less than that of to_inclusive"
        in error_response.content
    )


def test_records_response(client):
    response = client.get("/records", headers=api_key_headers)
    # Some trivial response validation:
    #  - The response should contain records when the request included no date filters.
    #  - Each record should have:
    #    - A properly-formatted from_inclusive date.
    #    - A properly-formatted to_inclusive date.
    #    - A value for duration greater than or equal to 5
    #    - A value for number_tropical_days greater than or equal to 3
    #    - A value for max_temperature greater than or equal to 30.0.
    records = response.json()
    assert len(records) > 0
    expected_date_format = re.compile(r"\d{4}-\d{2}-\d{2}")
    for record in records:
        assert expected_date_format.fullmatch(record["from_inclusive"]) is not None
        assert expected_date_format.fullmatch(record["to_inclusive"]) is not None
        assert record["duration"] >= 5
        assert record["number_tropical_days"] >= 3
        assert record["max_temperature"] >= 30.0
