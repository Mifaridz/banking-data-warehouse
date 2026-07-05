import urllib.parse

# KONFIGURASI SOURCE DATABASE SAMPLE.BAK
SQL_SERVER_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server", 
    "server": "localhost",
    "port": "1433",
    "database": "SampleSource",
    "user": "sa",
    "password": "RakaminDE_2026"
}

# KONFIGURASI TARGET DWH
DWH_CONFIG = {
    "driver": "ODBC Driver 17 for SQL Server", 
    "server": "localhost",
    "port": "1433",
    "database": "DWH", 
    "user": "sa",
    "password": "RakaminDE_2026"
}

def get_sql_alchemy_uri() -> str:
    cfg = SQL_SERVER_CONFIG
    safe_password = urllib.parse.quote_plus(cfg['password'])
    driver = cfg['driver'].replace(' ', '+')
    
    return f"mssql+pyodbc://{cfg['user']}:{safe_password}@{cfg['server']}:{cfg['port']}/{cfg['database']}?driver={driver}"

def get_dwh_uri() -> str:
    cfg = DWH_CONFIG
    safe_password = urllib.parse.quote_plus(cfg['password'])
    driver = cfg['driver'].replace(' ', '+')
    
    return f"mssql+pyodbc://{cfg['user']}:{safe_password}@{cfg['server']}:{cfg['port']}/{cfg['database']}?driver={driver}"