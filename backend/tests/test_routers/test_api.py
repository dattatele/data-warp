from fastapi.testclient import TestClient
from api.main import app
import pytest

client = TestClient(app)

def test_paginated_response():
    response = client.post("/query", json={
        "table_name": "users",
        "sql_query": "SELECT id, name FROM users",
        "page": 2,
        "per_page": 10
    })
    assert response.status_code == 200
    assert "total_pages" in response.json()
    assert len(response.json()["data"]) <= 10

def test_table_schema():
    response = client.get("/tables/users/schema")
    assert response.status_code == 200
    assert any(col["name"] == "id" for col in response.json()["columns"])

def test_preview_endpoint():
    response = client.get("/preview/users?limit=5")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5