from pydantic import BaseModel
from typing import List, Dict, Any

class TableListResponse(BaseModel):
    tables: List[str]

class ColumnSchema(BaseModel):
    name: str
    type: str

class TableSchemaResponse(BaseModel):
    columns: List[ColumnSchema]

class QueryRequest(BaseModel):
    # The client sends the SQL query (without pagination) along with pagination parameters.
    sql_query: str
    page: int = 1
    per_page: int = 50

class QueryResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]

class PreviewResponse(BaseModel):
    columns: List[str]
    rows: List[List[Any]]

class PaginatedResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    per_page: int
    total_pages: int
