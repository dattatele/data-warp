from fastapi import APIRouter, HTTPException, Query
from api.schemas.models import PreviewResponse
from api.services.query import preview_table as preview_table_service

router = APIRouter()

@router.get("/{table_name}", response_model=PreviewResponse)
def preview_table(table_name: str, limit: int = Query(100, gt=0)):
    """
    GET /preview/{table_name}?limit=100
    Preview the first n rows of the specified table.
    """
    try:
        columns, rows = preview_table_service(table_name, limit)
        return {"columns": columns, "rows": rows}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
