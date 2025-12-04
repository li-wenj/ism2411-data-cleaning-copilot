"""
data_cleaning.py

This script cleans the raw sales data and saves a cleaned CSV file.
"""

import pandas as pd

# File paths inside the project
RAW_PATH = "data/raw/sales_data_raw.csv"
CLEAN_PATH = "data/processed/sales_data_clean.csv"

# This function loads the raw CSV into a DataFrame so we can clean it.
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# This function standardizes column names and renames prodname/qty.
def clean_column_names(df):
    # make names lower case with underscores
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))


    # rename short names to clearer ones
    rename_map = {}
    if "prodname" in df.columns:
        rename_map["prodname"] = "product_name"
    if "qty" in df.columns:
        rename_map["qty"] = "quantity"
    df = df.rename(columns=rename_map)

    return df

# This function trims spaces from product_name and category.
def clean_text_columns(df):
    for col in ["product_name", "category"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    return df

# This function makes price and quantity numeric and drops rows with missing values.
def handle_missing_values(df):
    # 4. Make price and quantity numeric.
    #    Why: They should be numbers so we can check and filter them.
    for col in ["price", "quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Drop rows with missing price or quantity.
    #    Why: A sale without price or quantity is incomplete.
    needed = [c for c in ["price", "quantity"] if c in df.columns]
    if needed:
        df = df.dropna(subset=needed)

    return df


# This function removes negative price/quantity rows and duplicate rows.
def remove_invalid_rows(df):
    # 6. Remove rows with negative price or quantity.
    #    Why: Negative values here are data errors.
    if "price" in df.columns:
        df = df[df["price"] >= 0]
    if "quantity" in df.columns:
        df = df[df["quantity"] >= 0]

    # 7. Drop exact duplicate rows.
    #    Why: We only want each valid sale once.
    df = df.drop_duplicates()

    return df


if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = clean_text_columns(df_clean)      # 👈 add this line
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())
