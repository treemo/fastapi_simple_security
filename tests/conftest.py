"""Pytest configuration.
"""
import os
import time

import pytest
from fastapi.testclient import TestClient

# The environment variable needs to be set before importing app
admin_key_value = "secret"
os.environ["FASTAPI_SIMPLE_SECURITY_SECRET"] = admin_key_value

from app.main import app  # pylint: disable=wrong-import-position
from fastapi_simple_security._sqlite_access import (  # pylint: disable=wrong-import-position
    sqlite_access,
)


@pytest.fixture
def admin_key():
    return admin_key_value


@pytest.fixture
def client():
    try:
        # We remove the existing db file
        os.remove("sqlite.db")
        # We had disk I/O errors without this
        time.sleep(0.1)
        # We re-create the file and tables
        sqlite_access.init_db()

    except FileNotFoundError:
        pass

    return TestClient(app)
