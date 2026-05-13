import os
from datetime import datetime

import oracledb
import pandas as pd

from config import TABLES

from minio import Minio

minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

conn = oracledb.connect(
    user = "hr",
    password = 'hr',
    host = 'localhost',
    port = 1521,
    service_name='XEPDB1' 
)

print("connected")

batch_time = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("extract/output", exist_ok=True)
for table in TABLES:
    print(f'\nExtracting table: {table}')
    query = f"select * from {table}"
    df = pd.read_sql(query, conn)

    df['ingestion_timestamp'] = str(datetime.now())
    df['source_table'] = table
    df['batch_id'] = batch_time

    output_path = f"extract/output/{table}_{batch_time}.parquet"
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
    df.to_parquet(output_path, index=False)
    minio_client.fput_object(
        "bronze",
        f"{table}/{batch_time}.parquet",
        output_path

    )
    print(f"Uploaded to MinIO: {table}/{batch_time}.parquet")


print("all extracted")