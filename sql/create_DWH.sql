-- 1. BUAT DATABASE DWH

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DWH')
BEGIN
    CREATE DATABASE DWH;
    PRINT 'Database DWH berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Database DWH sudah ada.';
END
GO

USE DWH;
GO

-- 2. Buat Tabel DimBranch (Master Cabang)
IF OBJECT_ID('DimBranch', 'U') IS NULL
BEGIN
    CREATE TABLE DimBranch (
        BranchID INT PRIMARY KEY,
        BranchName VARCHAR(255) NOT NULL,
        BranchAddress VARCHAR(500)
    );
    PRINT 'Tabel DimBranch berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Tabel DimBranch sudah ada.';
END

-- 3. Buat Tabel DimCustomer (Master Nasabah)
IF OBJECT_ID('DimCustomer', 'U') IS NULL
BEGIN
    CREATE TABLE DimCustomer (
        CustomerID INT PRIMARY KEY,
        CustomerName VARCHAR(255) NOT NULL,
        Address VARCHAR(500),
        CityName VARCHAR(255),
        StateName VARCHAR(255),
        Age INT,
        Gender VARCHAR(50),
        Email VARCHAR(255)
    );
    PRINT 'Tabel DimCustomer berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Tabel DimCustomer sudah ada.';
END

-- 4. Buat Tabel DimAccount (Master Rekening)
IF OBJECT_ID('DimAccount', 'U') IS NULL
BEGIN
    CREATE TABLE DimAccount (
        AccountID INT PRIMARY KEY,
        CustomerID INT,
        AccountType VARCHAR(100),
        Balance DECIMAL(18, 2),
        DateOpened DATE,
        Status VARCHAR(50),
        FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID)
    );
    PRINT 'Tabel DimAccount berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Tabel DimAccount sudah ada.';
END

-- 5. Buat Tabel FactTransaction (Tabel Transaksi)
IF OBJECT_ID('FactTransaction', 'U') IS NULL
BEGIN
    CREATE TABLE FactTransaction (
        TransactionID INT PRIMARY KEY,
        AccountID INT,
        CustomerID INT,
        TransactionDate DATE,
        Amount DECIMAL(18, 2),
        TransactionType VARCHAR(100),
        BranchID INT,
        FOREIGN KEY (AccountID) REFERENCES DimAccount(AccountID),
        FOREIGN KEY (BranchID) REFERENCES DimBranch(BranchID)
    );
    PRINT 'Tabel FactTransaction berhasil dibuat.';
END
ELSE
BEGIN
    PRINT 'Tabel FactTransaction sudah ada.';
END
GO