import pandas as pd

def transform_dim_customer(df_customer, df_city, df_state) -> pd.DataFrame:
    print("[TRANSFORM] Memproses DimCustomer...")

    # 1. Gabung customer dengan city dan state
    df_joined = df_customer.merge(df_city, on="city_id", how="left")
    df_joined = df_joined.merge(df_state, on="state_id", how="left")

    df_dim = df_joined[[
        "customer_id", "customer_name", "address", "city_name", "state_name", "age", "gender", "email"
    ]].copy()

    # 2. Ubah semua string menjadi uppercase
    cols_to_upper = ["customer_name", "address", "city_name", "state_name", "gender"]
    for col in cols_to_upper:
        df_dim[col] = df_dim[col].apply(lambda x: str(x).upper() if pd.notna(x) else x)

    # 3. Rename kolom menjadi PascalCase
    df_dim = df_dim.rename(columns={
        "customer_id": "CustomerID",
        "customer_name": "CustomerName",
        "address": "Address",
        "city_name": "CityName",
        "state_name": "StateName",
        "age": "Age",
        "gender": "Gender",
        "email": "Email"
    })
    return df_dim

def transform_fact_transaction(df_db, df_csv, df_excel, df_account) -> pd.DataFrame:
    print("[TRANSFORM] Memproses FactTransaction...")

    # 1. Standardisasi nama kolom df_db ke snake_case agar sinkron saat concat
    df_db_cleaned = df_db.rename(columns={
        "TransactionID": "transaction_id",
        "AccountID": "account_id",
        "TransactionDate": "transaction_date",
        "Amount": "amount",
        "TransactionType": "transaction_type",
        "BranchID": "branch_id"
    }, errors="ignore")
    df_db_cleaned["transaction_date"] = pd.to_datetime(df_db_cleaned["transaction_date"]).dt.date

    # 2. Parsing tanggal CSV (Format ISO: YYYY-MM-DD)
    df_csv_cleaned = df_csv.copy()
    df_csv_cleaned["transaction_date"] = pd.to_datetime(df_csv_cleaned["transaction_date"], dayfirst=True).dt.date

    # 3. Parsing tanggal Excel menggunakan dayfirst=True (Format: DD-MM-YYYY)
    df_excel_cleaned = df_excel.copy()
    df_excel_cleaned["transaction_date"] = pd.to_datetime(df_excel_cleaned["transaction_date"], dayfirst=True).dt.date

    df_unified = pd.concat([df_db_cleaned, df_csv_cleaned, df_excel_cleaned], ignore_index=True)
    df_clean = df_unified.drop_duplicates(subset=["transaction_id"], keep="first").copy()

    # 4. Mencegah Duplikasi Amount! 
    df_account_lookup = df_account[["account_id", "customer_id"]].drop_duplicates(subset=["account_id"], keep="first")
    
    # 5. Tarik customer_id dari tabel account
    df_fact = df_clean.merge(df_account_lookup, on="account_id", how="left")
    df_fact["amount"] = pd.to_numeric(df_fact["amount"])

    # 6. Rename kolom menjadi PascalCase
    df_fact = df_fact.rename(columns={
        "transaction_id": "TransactionID",
        "account_id": "AccountID",
        "customer_id": "CustomerID",
        "transaction_date": "TransactionDate",
        "amount": "Amount",
        "transaction_type": "TransactionType",
        "branch_id": "BranchID"
    })
    
    target_columns = ["TransactionID", "AccountID", "CustomerID", "BranchID", "TransactionDate", "Amount", "TransactionType"]
    return df_fact[target_columns]


def transform_dim_account(df_account) -> pd.DataFrame:

    print("[TRANSFORM] Memproses DimAccount ke PascalCase...")
    return df_account.rename(columns={
        "account_id": "AccountID",
        "customer_id": "CustomerID",
        "date_opened": "DateOpened",
        "account_type": "AccountType",
        "balance": "Balance",
        "status": "Status"
    })

def transform_dim_branch(df_branch) -> pd.DataFrame:
    
    print("[TRANSFORM] Memproses DimBranch ke PascalCase...")
    return df_branch.rename(columns={
        "branch_id": "BranchID",
        "branch_name": "BranchName",
        "branch_location": "BranchAddress"
    })


# ORCHESTRATOR TRANSFORMASI
def transform_all_data(extracted_data: dict) -> dict:
    print("=== MEMULAI PROSES TRANSFORMASI DATA ===")
    
    transformed_data = {}

    # 1. Transformasi Tabel Dimensi (DimCustomer, DimAccount, DimBranch)
    transformed_data["DimAccount"] = transform_dim_account(extracted_data["account"])
    
    transformed_data["DimBranch"] = transform_dim_branch(extracted_data["branch"])
    
    transformed_data["DimCustomer"] = transform_dim_customer(
        df_customer=extracted_data["customer"],
        df_city=extracted_data["city"],
        df_state=extracted_data["state"]
    )

    # 2. Transformas Tabel Fakta (FactTransaction)
    transformed_data["FactTransaction"] = transform_fact_transaction(
        df_db=extracted_data["transaction_db"],
        df_csv=extracted_data["transaction_csv"],
        df_excel=extracted_data["transaction_excel"],
        df_account=extracted_data["account"] 
    )

    print("=== PROSES TRANSFORMASI DATA SELESAI ===")
    return transformed_data
