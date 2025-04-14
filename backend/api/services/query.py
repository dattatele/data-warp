from api.services.database import get_connection
from api.services.tables import list_tables

def execute_query(sql_query: str, page: int, per_page: int) -> dict:
    """
    Executes a SQL query with pagination and returns columns and rows.
    The function appends LIMIT and OFFSET to the provided SQL.
    """
    conn = get_connection()
    offset = (page - 1) * per_page
    paginated_query = f"{sql_query} LIMIT {per_page} OFFSET {offset}"
    cur = conn.execute(paginated_query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return {"columns": columns, "rows": rows}

def preview_table(table_name: str, limit: int):
    """
    Executes a SELECT * query on the specified table limited to n rows.
    """
    conn = get_connection()
    # Ensure the table exists
    if table_name not in list_tables():
        raise ValueError("Table not found")
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    cur = conn.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return columns, rows
