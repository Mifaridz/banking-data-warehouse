import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from etl.config.db_config import get_dwh_uri
from etl.validation.validation import (
    validate_dim_account,
    validate_dim_branch,
    validate_dim_customer,
    validate_fact_transaction,
    validate_foreign_key_values,
)

def load_table_upsert(df: pd.DataFrame, table_name: str, pk_col: str, engine) -> None:
    if df.empty:
        print(f"[LOAD] Tabel {table_name} kosong, dilewati.")
        return

    staging_table = f"stg_{table_name}"
    print(f"[LOAD] Memasukkan {len(df)} baris ke staging table '{staging_table}'...")

    # 1. Load data ke tabel sementara di SQL Server
    df.to_sql(
        name=staging_table, 
        con=engine, 
        if_exists='replace', 
        index=False
    )

    # 2. Susun query dinamis MERGE
    columns = df.columns.tolist()
    update_set = ", ".join([f"TARGET.{col} = SOURCE.{col}" for col in columns if col != pk_col])
    insert_cols = ", ".join(columns)
    insert_vals = ", ".join([f"SOURCE.{col}" for col in columns])

    merge_query = f"""
    MERGE {table_name} AS TARGET
    USING {staging_table} AS SOURCE
    ON TARGET.{pk_col} = SOURCE.{pk_col}
    WHEN MATCHED THEN
        UPDATE SET {update_set}
    WHEN NOT MATCHED BY TARGET THEN
        INSERT ({insert_cols})
        VALUES ({insert_vals});
    """

    # 3. Eksekusi MERGE dan hapus tabel staging dalam satu Transaction
    try:
        with engine.begin() as conn:
            print(f"[LOAD] Menjalankan operasi UPSERT ke tabel utama '{table_name}'...")
            conn.execute(text(merge_query))
            conn.execute(text(f"DROP TABLE {staging_table};"))
        print(f"[LOAD] Sukses UPSERT data ke {table_name}.\n")
    except SQLAlchemyError as e:
        print(f"[ERROR] Gagal melakukan UPSERT pada tabel {table_name}: {e}")
        raise e

def load_all_data(transformed_data: dict) -> None:
    uri = get_dwh_uri()
    engine = create_engine(uri)

    df_fact = transformed_data["FactTransaction"]
    df_acc = transformed_data["DimAccount"]
    df_branch = transformed_data["DimBranch"]
    df_customer = transformed_data["DimCustomer"]

    print("[VALIDATION] Memulai validasi data sebelum load...")
    validate_dim_customer(df_customer)
    validate_dim_account(df_acc)
    validate_dim_branch(df_branch)
    validate_fact_transaction(df_fact)
    validate_foreign_key_values(df_fact, "AccountID", df_acc, "AccountID", strict=False)
    validate_foreign_key_values(df_fact, "BranchID", df_branch, "BranchID", strict=False)

    valid_accounts = df_acc["AccountID"].unique()
    initial_len = len(df_fact)

    transformed_data["FactTransaction"] = df_fact[df_fact["AccountID"].isin(valid_accounts)]
    filtered_len = len(transformed_data["FactTransaction"])

    if initial_len != filtered_len:
        print(f"[WARNING DATA KOTOR] Membuang {initial_len - filtered_len} baris dari FactTransaction karena AccountID tidak terdaftar di DimAccount!\n")

    try:
        load_table_upsert(transformed_data["DimBranch"], "DimBranch", "BranchID", engine)
        load_table_upsert(transformed_data["DimCustomer"], "DimCustomer", "CustomerID", engine)
        load_table_upsert(transformed_data["DimAccount"], "DimAccount", "AccountID", engine)
        load_table_upsert(transformed_data["FactTransaction"], "FactTransaction", "TransactionID", engine)

        print("=== PROSES LOAD SELESAI DENGAN SUKSES ===")

    except SQLAlchemyError as e:
        print(f"\n[ERROR FATAL] Proses Load Gagal!")
        print(f"[ERROR DETAILED] Pesan: {e}")
        raise e