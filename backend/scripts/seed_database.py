# import pandas as pd
# from pathlib import Path
# from faker import Faker
# from api.core.config import settings
# from api.services.database import get_db_connection

# def generate_data():
#     fake = Faker()
    
#     # Generate Users
#     users = pd.DataFrame([{
#         "id": i,
#         "name": fake.name(),
#         "email": fake.email(),
#         "created_at": fake.date_time_this_decade()
#     } for i in range(1, 10001)])
    
#     # Generate Products
#     products = pd.DataFrame([{
#         "id": i,
#         "name": fake.word().title(),
#         "price": round(fake.random.uniform(1, 1000), 2),
#         "in_stock": fake.boolean()
#     } for i in range(1, 10001)])
    
#     # Save to Parquet
#     users.to_parquet(Path(settings.parquet_dir) / "users.parquet")
#     products.to_parquet(Path(settings.parquet_dir) / "products.parquet")

# def register_tables():
#     with get_db_connection() as conn:
#         # Verify tables
#         tables = conn.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_type = 'VIEW'
#         """).fetchall()
#         print("Registered tables:", [t[0] for t in tables])

# if __name__ == "__main__":
#     generate_data()
#     register_tables()
#     print("✅ Database seeded successfully!")


import duckdb
import pandas as pd
import numpy as np
import os

def seed_database():
    # Set up paths for the data directory and files.
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Number of rows per table.
    num_rows = 10_000

    # Base timestamp for generating date/time values.
    base_time = pd.Timestamp("2024-01-01")

    # --- Create DataFrames with sample data ---
    # Create sales_data DataFrame.
    sales_data = pd.DataFrame({
        "id": np.arange(1, num_rows + 1),
        "created_at": [base_time + pd.Timedelta(minutes=i) for i in range(1, num_rows + 1)],
        "amount": np.round(np.random.uniform(10.0, 500.0, size=num_rows), 2)
    })
    print("Sales data generated.")

    # Create events_stream DataFrame.
    events_stream = pd.DataFrame({
        "id": np.arange(1, num_rows + 1),
        "event_name": [f"Event_{np.random.randint(1, 101)}" for _ in range(num_rows)],
        "event_time": [base_time + pd.Timedelta(minutes=i) for i in range(1, num_rows + 1)]
    })
    print("Events stream data generated.")

    # --- Write DataFrames to Parquet files ---
    sales_parquet_path = os.path.join(data_dir, "sales_data.parquet")
    events_parquet_path = os.path.join(data_dir, "events_stream.parquet")
    
    sales_data.to_parquet(sales_parquet_path, index=False)
    events_stream.to_parquet(events_parquet_path, index=False)

    # --- Create or update the DuckDB database ---
    db_path = os.path.join(data_dir, "duckdb.db")
    conn = duckdb.connect(database=db_path, read_only=False)

    # Drop tables if they already exist.
    conn.execute("DROP TABLE IF EXISTS sales_data;")
    conn.execute("DROP TABLE IF EXISTS events_stream;")

    # Create tables by reading the respective Parquet files.
    conn.execute(f"CREATE TABLE sales_data AS SELECT * FROM read_parquet('{sales_parquet_path}');")
    conn.execute(f"CREATE TABLE events_stream AS SELECT * FROM read_parquet('{events_parquet_path}');")

    conn.commit()
    conn.close()
    print("Database seeded successfully using parquet files.")

if __name__ == "__main__":
    seed_database()
    print("✅ Database seeded successfully!")