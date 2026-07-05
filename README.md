# Banking Data Warehouse ETL Project

Project ini adalah contoh implementasi ETL sederhana untuk membangun data warehouse banking dari beberapa sumber data: SQL Server, CSV, dan Excel. Alur kerja ini mencakup ekstraksi, transformasi, validasi, dan loading ke data warehouse lokal berbasis SQL Server.

## Tujuan Project

Tujuan utama project ini adalah untuk:

- mengekstrak data dari beberapa sumber
- membersihkan dan menstandarkan data agar siap dianalisis
- melakukan validasi sebelum data dimuat ke warehouse
- memuat data terstruktur ke SQL Server untuk kebutuhan analitik

## Alur ETL

1. Extract
   - membaca data dari tabel SQL Server
   - membaca data dari file CSV
   - membaca data dari file Excel

2. Transform
   - menggabungkan data transaksi dari beberapa sumber
   - menghapus data duplikat
   - menstandarkan nama kolom dan nilai
   - menghasilkan tabel dimensi dan tabel fakta

3. Validate
   - memastikan kolom wajib ada
   - memastikan primary key tidak null atau duplikat
   - memvalidasi field penting sebelum loading
   - mencegah data tidak valid masuk ke warehouse

4. Load
   - memuat data ke SQL Server menggunakan logika UPSERT
   - mengisi tabel seperti DimCustomer, DimAccount, DimBranch, dan FactTransaction

## Struktur Project

```text
banking-data-warehouse/
├── data_source/                 # file input dan data backup
├── etl/
│   ├── config/                  # konfigurasi database
│   ├── extract/                 # modul ekstraksi
│   ├── load/                    # modul loading
│   ├── transform/               # modul transformasi
│   └── validation/              # modul validasi
├── main.py                      # entry point ETL utama
├── docker-compose.yml           # Docker Compose untuk SQL Server
├── requirements.txt             # dependency Python
└── README.md                    # dokumentasi project
```

## Persyaratan Sistem

Pastikan hal-hal berikut sudah tersedia:

- Python 3.10+
- Docker dan Docker Compose (disarankan untuk SQL Server)
- ODBC Driver 17 for SQL Server
- akses ke instance SQL Server lokal atau container

## Clone Repository

```bash
git clone <repo-url>
cd banking-data-warehouse
```

## Setup Environment Python

Buat dan aktifkan virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.\.venv\Scripts\activate       # Windows
```

Install dependency:

```bash
pip install -r requirements.txt
```

## Menjalankan SQL Server dengan Docker

Jalankan container SQL Server:

```bash
docker compose up -d
```

Cek apakah container berjalan:

```bash
docker compose ps
```

## Menjalankan Pipeline ETL

Jalankan file utama project:

```bash
python main.py
```

## Output yang Diharapkan

Proses yang berhasil akan menampilkan log seperti berikut:

```text
=== Memulai Proses ETL ===
=== Extract Data ===
[EXTRACT] Membaca tabel customer dari SQL Server...
[EXTRACT] Membaca file CSV dari data_source/transaction_csv.csv...
[EXTRACT] Membaca file Excel dari data_source/transaction_excel.xlsx...

=== Transform Data ===
[TRANSFORM] Memproses DimCustomer (tMap logic)...
[TRANSFORM] Memproses FactTransaction (tUnite & tUniq Logic)...

=== MEMULAI PROSES LOAD DATA ===
[VALIDATION] Memulai validasi data sebelum load...
[LOAD] Sukses UPSERT data ke DimBranch.
[LOAD] Sukses UPSERT data ke DimCustomer.
[LOAD] Sukses UPSERT data ke DimAccount.
[LOAD] Sukses UPSERT data ke FactTransaction.

=== PROSES LOAD SELESAI DENGAN SUKSES ===
```

## Hasil yang Diharapkan di SQL Server

Jika proses berhasil, tabel berikut akan terisi di database DWH:

- DimBranch
- DimCustomer
- DimAccount
- FactTransaction

## Menjalankan Test Validasi

Untuk memverifikasi modul validasi:

```bash
python -m unittest tests.test_validation
```

## Catatan

- File sensitif seperti credential, variabel environment, dan state lokal sudah disembunyikan melalui .gitignore.
- Repository ini juga dilengkapi dengan file Docker Compose untuk pengembangan lebih lanjut, termasuk skenario dengan Airflow.

## Pengembangan Selanjutnya

Beberapa peningkatan yang bisa ditambahkan ke project ini:

- logging yang lebih terstruktur
- penjadwalan otomatis
- monitoring dan alerting
- integrasi dengan cloud data warehouse
- validasi business rule yang lebih kompleks
