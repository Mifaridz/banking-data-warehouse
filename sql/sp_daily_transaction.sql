USE DWH;
GO

-- Menghapus SP jika sudah ada
IF OBJECT_ID('dbo.DailyTransaction', 'P') IS NOT NULL
    DROP PROCEDURE dbo.DailyTransaction;
GO

-- Membuat SP Utama secara langsung
CREATE PROCEDURE dbo.DailyTransaction
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        CAST(TransactionDate AS DATE) AS [Date],
        COUNT(TransactionID) AS TotalTransactions,
        SUM(Amount) AS TotalAmount
    FROM dbo.FactTransaction
    WHERE TransactionDate BETWEEN @start_date AND @end_date
    GROUP BY CAST(TransactionDate AS DATE)
    ORDER BY [Date];
END;
GO

PRINT 'SP DailyTransaction berhasil dibuat.';
GO