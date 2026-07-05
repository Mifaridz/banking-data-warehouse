import pandas as pd
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from etl.config.db_config import get_sql_alchemy_uri

def extract_from_sql_server(table_name: str) -> pd.DataFrame:
    """Mengambil data dari SQL Server."""
    print(f"[EXTRACT] Membaca tabel {table_name} dari SQL Server...")
    try:
        uri = get_sql_alchemy_uri()
        engine = create_engine(uri)
        
        with engine.connect() as connection:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, con=connection)
            return df
            
    except SQLAlchemyError as e:
        print(f"[ERROR] Gagal mengekstrak tabel {table_name}: {e}")
        sys.exit(1)

def extract_from_csv(file_path: str) -> pd.DataFrame:
    """Mengambil data dari file CSV ."""
    print(f"[EXTRACT] Membaca file CSV dari {file_path}...")
    if not os.path.exists(file_path):
        print(f"[ERROR] File CSV tidak ditemukan di {file_path}")
        sys.exit(1)
        
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"[ERROR] Gagal membaca CSV {file_path}: {e}")
        sys.exit(1)

def extract_from_excel(file_path: str, sheet_name: str | int = 0) -> pd.DataFrame:
    """Mengambil data dari file Excel."""
    print(f"[EXTRACT] Membaca file Excel dari {file_path}...")
    if not os.path.exists(file_path):
        print(f"[ERROR] File Excel tidak ditemukan di {file_path}")
        sys.exit(1)
        
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"[ERROR] Gagal membaca Excel {file_path}: {e}")
        sys.exit(1)

# ==========================================
# ORCHESTRATOR 
# ==========================================

def extract_all_data(csv_path: str, excel_path: str) -> dict:

    print("=== MEMULAI PROSES EKSTRAKSI DATA ===")
    
    # Dictionary untuk menyimpan seluruh dataframe
    extracted_data = {}

    # 1. Ekstrak Data Transaksi (3 Source Berbeda)
    extracted_data['transaction_excel'] = extract_from_excel(excel_path)
    extracted_data['transaction_csv'] = extract_from_csv(csv_path)
    extracted_data['transaction_db'] = extract_from_sql_server('transaction_db')

    # 2. Ekstrak Master Data (Dimensi) dari SQL Server
    tables_to_extract = ['account', 'customer', 'branch', 'city', 'state']
    
    for table in tables_to_extract:
        extracted_data[table] = extract_from_sql_server(table)
        
    print("=== PROSES EKSTRAKSI DATA SELESAI ===")
    return extracted_data

if __name__ == "__main__":
    CSV_FILE_PATH = "./data/source/transaction_csv.csv"
    EXCEL_FILE_PATH = "./data/source/transaction_excel.xlsx"
    
    # Menampung semua data
    data_raw = extract_all_data(csv_path=CSV_FILE_PATH, excel_path=EXCEL_FILE_PATH)
    
    # Validasi data yang berhasil diekstrak
    print(f"Total baris transaksi Excel: {len(data_raw['transaction_excel'])}")
    print(f"Total baris tabel nasabah: {len(data_raw['customer'])}")