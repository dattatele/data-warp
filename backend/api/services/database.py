import duckdb
from api.core.config import settings

_connection = None

def get_connection() -> duckdb.DuckDBPyConnection:
    global _connection
    if _connection is None:
        _connection = duckdb.connect(database=settings.DUCKDB_PATH, read_only=False)
    return _connection
