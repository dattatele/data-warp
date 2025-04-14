from fastapi import FastAPI
from api.routers import tables, query, preview

app = FastAPI(
    title="DuckDB API",
    description="API for listing DuckDB tables, viewing schemas, executing queries and previewing data with pagination.",
    version="0.1.0"
)

app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(preview.router, prefix="/preview", tags=["preview"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




# app.include_router(tables.router, prefix="/api/v1")
# app.include_router(query.router, prefix="/api/v1")