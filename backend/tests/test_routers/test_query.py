# from fastapi.testclient import TestClient
# from unittest.mock import patch
# import duckdb
# import pytest

# from backend.api.routers.query import router

# client = TestClient(router)

# @patch("backend.api.services.database.get_db_connection")
# def test_query_endpoint(mock_conn):
#     mock_conn.return_value.__enter__.return_value.execute.return_value.fetchall.return_value = [("test",)]
    
#     response = client.post("/query", json={
#         "table_name": "users",
#         "sql_query": "SELECT * FROM users",
#         "page": 1,
#         "per_page": 10
#     })
    
#     assert response.status_code == 200
#     assert "data" in response.json()


import pytest

def test_execute_query(test_client):
    # Use an existing table from the seeded data
    list_resp = test_client.get("/tables/")
    tables = list_resp.json().get("tables", [])
    if not tables:
        pytest.skip("No tables available in database")
    table = tables[0]
    sql_query = f"SELECT * FROM {table}"
    payload = {"sql_query": sql_query, "page": 1, "per_page": 10}
    response = test_client.post("/query/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data and "rows" in data

def test_preview_table_not_found(test_client):
    response = test_client.get("/preview/non_existent_table")
    # Our implementation raises HTTP 400 when table is not found
    assert response.status_code == 400

def test_preview_table(test_client):
    list_resp = test_client.get("/tables/")
    tables = list_resp.json().get("tables", [])
    if not tables:
        pytest.skip("No tables available in database")
    table = tables[0]
    response = test_client.get(f"/preview/{table}?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data and "rows" in data
