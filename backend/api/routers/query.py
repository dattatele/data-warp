from fastapi import APIRouter, HTTPException
from api.schemas.models import QueryRequest, QueryResponse
from api.services.query import execute_query as execute_query_service

router = APIRouter()

@router.post("/", response_model=QueryResponse)
def execute_query(query_request: QueryRequest):
    """
    POST /query
    Execute a user-provided SQL query with pagination.
    """
    try:
        result = execute_query_service(query_request.sql_query, query_request.page, query_request.per_page)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
