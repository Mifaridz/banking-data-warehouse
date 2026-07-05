import os
from etl.extract.extract import (
    extract_from_sql_server,
    extract_from_csv,
    extract_from_excel
)
from etl.transform.transform import (
    transform_dim_account,
    transform_dim_branch,
    transform_dim_customer,
    transform_fact_transaction
)
from etl.load.load import load_all_data
# from etl.load.bq_loader import BigQueryLoader

def main():
    print("=== Memulai Proses ETL ===")

    # 1. EXTRACT: Mengambil data dari sumber
    print("\n=== Extract Data ===")
    
    # Extract: Mengambil data dari SQL Server
    df_customer = extract_from_sql_server("customer")
    df_city = extract_from_sql_server("city")
    df_state = extract_from_sql_server("state")
    df_account = extract_from_sql_server("account")
    df_branch = extract_from_sql_server("branch")
    df_transaction_db = extract_from_sql_server("transaction_db")

    # Extract: Mengambil data dari CSV
    path_csv = "data_source/transaction_csv.csv"
    df_transaction_csv = extract_from_csv(path_csv)

    # Extract: Mengambil data dari Excel
    path_excel = "data_source/transaction_excel.xlsx"
    df_transaction_excel = extract_from_excel(path_excel)

    print("\n=== Extract Selesai. Ukuran Data Mentah: ===")
    print(f"Customer DB: {df_customer.shape}")
    print(f"City DB: {df_city.shape}")
    print(f"State DB: {df_state.shape}")
    print(f"Account DB: {df_account.shape}")
    print(f"Branch DB: {df_branch.shape}")
    print(f"Transaction DB: {df_transaction_db.shape}")
    print(f"Transaction CSV: {df_transaction_csv.shape}")
    print(f"Transaction Excel: {df_transaction_excel.shape}")


    # 2. TRANSFORM: Memproses data mentah
    print("\n=== Transform Data ===")

    # Transform Tabel Dimensional
    df_dim_customer = transform_dim_customer(df_customer, df_city, df_state)
    df_dim_account = transform_dim_account(df_account)
    df_dim_branch = transform_dim_branch(df_branch)

    # Transform Tabel Fakta (Menambahkan df_account untuk lookup CustomerID)
    df_fact_transaction = transform_fact_transaction(
        df_transaction_db, 
        df_transaction_csv, 
        df_transaction_excel, 
        df_account
    )

    print("\n=== Transform Selesai. Ukuran Data Hasil Transform: ===")
    print(f"DimCustomer: {df_dim_customer.shape}")
    print(f"DimAccount: {df_dim_account.shape}")
    print(f"DimBranch: {df_dim_branch.shape}")
    print(f"FactTransaction: {df_fact_transaction.shape}")

    # 3. LOAD : Memasukkan data ke DWH
    print("\n=== MEMULAI PROSES LOAD DATA ===")
    
    # Kumpulkan DataFrame yang sudah bersih ke dalam satu dictionary
    dict_transformed_data = {
        "DimBranch": df_dim_branch,
        "DimCustomer": df_dim_customer,
        "DimAccount": df_dim_account,
        "FactTransaction": df_fact_transaction
    }
    
    # --- 3A. LOAD KE SQL SERVER LOKAL ---
    print("\n>>> Target 1: DWH SQL Server Lokal")
    load_all_data(dict_transformed_data)
    print("Sukses Load ke SQL Server Lokal.")

    # --- 3B. LOAD KE GOOGLE BIGQUERY ---
    # print("\n>>> Target 2: Google BigQuery (GCP)")
    # GCP_PROJECT_ID = "banking-dwh-project" 
    # BUCKET_NAME = f"{GCP_PROJECT_ID}-data-lake"
    # BIGQUERY_DATASET = "DWH"

    # try:
    #     # Inisiasi koneksi ke GCP menggunakan Loader kita
    #     bq_loader = BigQueryLoader(project_id=GCP_PROJECT_ID, bucket_name=BUCKET_NAME)
        
    #     # Lakukan perulangan (looping) untuk setiap tabel dalam dictionary
    #     for table_name, df_table in dict_transformed_data.items():
    #         print(f"⚡ Ingesting {table_name} ke BigQuery...")
    #         bq_loader.load_data_to_bigquery(
    #             df=df_table,
    #             dataset_id=BIGQUERY_DATASET,
    #             table_id=table_name,
    #             load_mode="replace" # Menggunakan replace agar menimpa data lama (Idempotent)
    #         )
    #     print("\n=== SELURUH PROSES ETL (LOCAL + CLOUD) BERHASIL ===")
    
    # except Exception as e:
    #     print(f"\n❌ GAGAL MENGUNGGAH KE BIGQUERY: {e}")


if __name__ == "__main__":
    main()