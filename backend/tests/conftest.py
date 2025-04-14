# import pytest
# from fastapi.testclient import TestClient
# from api.routers import tables, query  # Updated import
# from api.core.config import settings  # Updated import

# @pytest.fixture
# def client():
#     from run import app
#     return TestClient(app)

# @pytest.fixture
# def test_db():
#     test_db_path = "/tmp/test_duck.db"
#     settings.duckdb_path = test_db_path
#     yield
#     import os
#     if os.path.exists(test_db_path):
#         os.remove(test_db_path)

import pytest
from fastapi.testclient import TestClient
from run import app

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
