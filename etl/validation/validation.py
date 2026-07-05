import pandas as pd


def validate_required_columns(dataframe: pd.DataFrame, required_columns: list[str]) -> bool:
    missing_columns = [column for column in required_columns if column not in dataframe.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return True


def validate_no_null_primary_key(dataframe: pd.DataFrame, primary_key: str) -> bool:
    null_count = dataframe[primary_key].isna().sum()

    if null_count > 0:
        raise ValueError(f"Primary key {primary_key} contains {null_count} null values")

    return True


def validate_no_duplicate_primary_key(dataframe: pd.DataFrame, primary_key: str) -> bool:
    duplicate_count = dataframe.duplicated(subset=[primary_key]).sum()

    if duplicate_count > 0:
        raise ValueError(f"Primary key {primary_key} contains {duplicate_count} duplicate values")

    return True


def validate_dim_customer(dataframe: pd.DataFrame) -> bool:
    required_columns = [
        "CustomerID",
        "CustomerName",
        "Address",
        "CityName",
        "StateName",
        "Age",
        "Gender",
        "Email",
    ]

    validate_required_columns(dataframe, required_columns)
    validate_no_null_primary_key(dataframe, "CustomerID")
    validate_no_duplicate_primary_key(dataframe, "CustomerID")
    return True


def validate_dim_account(dataframe: pd.DataFrame) -> bool:
    required_columns = [
        "AccountID",
        "CustomerID",
        "AccountType",
        "Balance",
        "DateOpened",
        "Status",
    ]

    validate_required_columns(dataframe, required_columns)
    validate_no_null_primary_key(dataframe, "AccountID")
    validate_no_duplicate_primary_key(dataframe, "AccountID")

    null_customer_id_count = dataframe["CustomerID"].isna().sum()
    if null_customer_id_count > 0:
        raise ValueError(f"CustomerID contains {null_customer_id_count} null values")

    return True


def validate_dim_branch(dataframe: pd.DataFrame) -> bool:
    required_columns = ["BranchID", "BranchName", "BranchAddress"]

    validate_required_columns(dataframe, required_columns)
    validate_no_null_primary_key(dataframe, "BranchID")
    validate_no_duplicate_primary_key(dataframe, "BranchID")
    return True


def validate_fact_transaction(dataframe: pd.DataFrame) -> bool:
    required_columns = [
        "TransactionID",
        "AccountID",
        "TransactionDate",
        "Amount",
        "TransactionType",
        "BranchID",
    ]

    validate_required_columns(dataframe, required_columns)
    validate_no_null_primary_key(dataframe, "TransactionID")
    validate_no_duplicate_primary_key(dataframe, "TransactionID")

    null_account_id_count = dataframe["AccountID"].isna().sum()
    null_branch_id_count = dataframe["BranchID"].isna().sum()
    null_transaction_date_count = dataframe["TransactionDate"].isna().sum()
    null_amount_count = dataframe["Amount"].isna().sum()

    if null_account_id_count > 0:
        raise ValueError(f"AccountID contains {null_account_id_count} null values")

    if null_branch_id_count > 0:
        raise ValueError(f"BranchID contains {null_branch_id_count} null values")

    if null_transaction_date_count > 0:
        raise ValueError(f"TransactionDate contains {null_transaction_date_count} null values")

    if null_amount_count > 0:
        raise ValueError(f"Amount contains {null_amount_count} null values")

    return True


def validate_foreign_key_values(
    dataframe: pd.DataFrame,
    column_name: str,
    reference_dataframe: pd.DataFrame,
    reference_column: str,
    strict: bool = True,
) -> bool:
    source_values = set(dataframe[column_name].dropna().unique())
    reference_values = set(reference_dataframe[reference_column].dropna().unique())

    invalid_values = source_values - reference_values

    if invalid_values:
        message = f"Invalid foreign key values found in {column_name}: {invalid_values}"
        if strict:
            raise ValueError(message)
        print(f"[WARNING] {message}")

    return True
