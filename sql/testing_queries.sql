USE DWH;
GO

-- A. DATA QUALITY CHECKS

PRINT '--- 1. Cek total baris di semua tabel DWH ---';
SELECT 'DimCustomer' AS TableName, COUNT(*) AS TotalRows FROM dbo.DimCustomer
UNION ALL
SELECT 'DimAccount', COUNT(*) FROM dbo.DimAccount
UNION ALL
SELECT 'DimBranch', COUNT(*) FROM dbo.DimBranch
UNION ALL
SELECT 'FactTransaction', COUNT(*) FROM dbo.FactTransaction;
GO

PRINT '--- 2. Cek duplikasi TransactionID di FactTransaction ---';
SELECT TransactionID, COUNT(*) AS TotalDuplicate 
FROM dbo.FactTransaction 
GROUP BY TransactionID 
HAVING COUNT(*) > 1;
GO

PRINT '--- 3. Cek duplikasi CustomerID di DimCustomer ---';
SELECT CustomerID, COUNT(*) AS TotalDuplicate 
FROM dbo.DimCustomer 
GROUP BY CustomerID 
HAVING COUNT(*) > 1;
GO

PRINT '--- 4. Cek duplikasi AccountID di DimAccount ---';
SELECT AccountID, COUNT(*) AS TotalDuplicate 
FROM dbo.DimAccount 
GROUP BY AccountID 
HAVING COUNT(*) > 1;
GO

PRINT '--- 5. Cek duplikasi BranchID di DimBranch ---';
SELECT BranchID, COUNT(*) AS TotalDuplicate 
FROM dbo.DimBranch 
GROUP BY BranchID 
HAVING COUNT(*) > 1;
GO

PRINT '--- 6. Cek invalid CustomerID di DimAccount (Orphan Data) ---';
SELECT da.* 
FROM dbo.DimAccount da 
LEFT JOIN dbo.DimCustomer dc ON da.CustomerID = dc.CustomerID 
WHERE dc.CustomerID IS NULL;
GO

PRINT '--- 7. Cek invalid AccountID di FactTransaction (Orphan Data) ---';
SELECT ft.* 
FROM dbo.FactTransaction ft 
LEFT JOIN dbo.DimAccount da ON ft.AccountID = da.AccountID 
WHERE da.AccountID IS NULL;
GO

PRINT '--- 8. Cek invalid BranchID di FactTransaction (Orphan Data) ---';
SELECT ft.* 
FROM dbo.FactTransaction ft 
LEFT JOIN dbo.DimBranch db ON ft.BranchID = db.BranchID 
WHERE db.BranchID IS NULL;
GO

PRINT '--- 9. Preview data akhir FactTransaction ---';
SELECT TOP 10 * 
FROM dbo.FactTransaction 
ORDER BY TransactionDate;
GO


-- B. TESTING STORED PROCEDURES

PRINT '--- 10. Test Stored Procedure: DailyTransaction ---';
DECLARE @MinDate DATE;
DECLARE @MaxDate DATE;

SELECT 
    @MinDate = MIN(TransactionDate), 
    @MaxDate = MAX(TransactionDate) 
FROM dbo.FactTransaction;
EXEC dbo.DailyTransaction 
    @start_date = @MinDate, 
    @end_date = @MaxDate;
GO

PRINT '--- 11. Test Stored Procedure: BalancePerCustomer ---';
EXEC dbo.BalancePerCustomer 
    @customer_name = 'Shelly';
GO