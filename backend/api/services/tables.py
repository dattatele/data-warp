from api.services.database import get_connection

def list_tables() -> list:
    """
    Returns a list of table names from the DuckDB database.
    """
    conn = get_connection()
    result = conn.execute("SHOW TABLES;").fetchall()
    # Assuming the first column of each result tuple is the table name.
    return [row[0] for row in result]

def get_table_schema(table_name: str) -> list:
    """
    Returns the schema for a table (list of dictionaries with column name and type).
    """
    conn = get_connection()
    try:
        result = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
        # Each row: (cid, name, type, notnull, dflt_value, pk)
        columns = [{"name": row[1], "type": row[2]} for row in result]
        return columns if columns else None
    except Exception:
        return None

def preview_table(table_name: str, limit: int):
    """
    Returns the columns and a preview (first n rows) of the given table.
    """
    # Validate table existence
    if table_name not in list_tables():
        raise ValueError("Table not found")
    conn = get_connection()
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    cur = conn.execute(query)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    return columns, rows
