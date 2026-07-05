USE DWH;
GO

-- Menghapus SP jika sudah ada
IF OBJECT_ID('dbo.BalancePerCustomer', 'P') IS NOT NULL
    DROP PROCEDURE dbo.BalancePerCustomer;
GO

-- Membuat SP Utama secara langsung
CREATE PROCEDURE dbo.BalancePerCustomer
    @customer_name VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        dc.CustomerName,
        da.AccountType,
        da.Balance,
        (da.Balance + ISNULL(SUM(
            CASE 
                WHEN UPPER(ft.TransactionType) = 'DEPOSIT' THEN ft.Amount
                ELSE -ft.Amount
            END
        ), 0)) AS CurrentBalance
    FROM dbo.DimAccount da
    JOIN dbo.DimCustomer dc ON da.CustomerID = dc.CustomerID
    LEFT JOIN dbo.FactTransaction ft ON da.AccountID = ft.AccountID
    WHERE dc.CustomerName LIKE '%' + @customer_name + '%'
      AND da.Status = 'ACTIVE'
    GROUP BY
        dc.CustomerName,
        da.AccountType,
        da.Balance,
        da.AccountID
    ORDER BY
        da.AccountType;
END;
GO

PRINT 'SP BalancePerCustomer berhasil dibuat.';
GO