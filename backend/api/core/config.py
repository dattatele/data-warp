# from pathlib import Path
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     db_path: str = "file::memory:?cache=shared"
#     parquet_dir: Path = Path("data/parquet")
    
#     def __init__(self):
#         super().__init__()
#         self.parquet_dir.mkdir(parents=True, exist_ok=True)

# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DUCKDB_PATH: str = "data/duckdb.db"  # Path to the DuckDB database file

    class Config:
        env_file = ".env"

settings = Settings()
