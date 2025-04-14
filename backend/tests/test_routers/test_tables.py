import pytest

def test_list_tables(test_client):
    response = test_client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert "tables" in data
    assert isinstance(data["tables"], list)

def test_get_table_schema_not_found(test_client):
    response = test_client.get("/tables/non_existent_table/schema")
    assert response.status_code == 404

def test_get_table_schema(test_client):
    # Use an existing table from the seeded data
    list_resp = test_client.get("/tables/")
    tables = list_resp.json().get("tables", [])
    if not tables:
        pytest.skip("No tables available in database")
    table = tables[0]
    schema_resp = test_client.get(f"/tables/{table}/schema")
    assert schema_resp.status_code == 200
    data = schema_resp.json()
    assert "columns" in data
    for column in data["columns"]:
        assert "name" in column and "type" in column
