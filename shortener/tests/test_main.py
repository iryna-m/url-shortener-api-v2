# This module contains unit tests for endpoints

import json

import pytest
import requests
from starlette.testclient import TestClient

from shortener import main
from shortener.main import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


def test_index_page(test_app):
    response = test_app.get("/")
    assert response.status_code == 200


def test_create_short_url(test_app):
    test_request_payload = {"original_url": "https://www.google.com/"}
    test_response_payload = {"original_url": "https://www.google.com/", "is_active": True, "clicks": 0,
                             "url": "http://127.0.0.1:8000/YM226",
                             "admin_url": "http://127.0.0.1:8000/admin/YM226_6FMNUEEG"}

    response = test_app.post("/url", data=json.dumps(test_request_payload), )

    assert response.status_code == 200
    # assert response.json() == test_response_payload


def test_send_invalid_url(test_app):
    response = test_app.post("/url", data=json.dumps({"original_url": "something"}))
    assert response.status_code == 400


def test_get_url_info(test_app):
    secret_key = "YM226_6FMNUEEG"
    test_data = {"original_url": "https://www.google.com/", "is_active": True, "clicks": 1,
                 "url": "http://127.0.0.1:8000/YM226",
                 "admin_url": "http://127.0.0.1:8000/admin/YM226_6FMNUEEG"}

    response = test_app.get("/default/administration_info_admin__secret_key__get")
    assert response.status_code == 200
