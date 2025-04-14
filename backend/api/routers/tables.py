from fastapi import APIRouter, HTTPException
from api.schemas.models import TableListResponse, TableSchemaResponse
from api.services.tables import list_tables as list_tables_service, get_table_schema as get_table_schema_service

router = APIRouter()

@router.get("/", response_model=TableListResponse)
def list_tables():
    """
    GET /tables
    List all available tables.
    """
    try:
        tables = list_tables_service()
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{table_name}/schema", response_model=TableSchemaResponse)
def get_table_schema(table_name: str):
    """
    GET /tables/{table_name}/schema
    Returns the schema (columns and types) for the selected table.
    """
    try:
        schema = get_table_schema_service(table_name)
        if schema is None:
            raise HTTPException(status_code=404, detail="Table not found")
        return {"columns": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
