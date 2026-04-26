import pandas as pd
import numpy as np
import os

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    print("Data loaded successfully.")
    print(f"Dataset shape: {df.shape}")
    return df

def basic_validation(df):
    print("\n--- Basic Validation ---")
    print(df.info())
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print(f"\nNumber of duplicate rows: {df.duplicated().sum()}")

if __name__ == "__main__":
    raw_data_path = 'data/raw/Online Retail.xlsx'
    
    # 1. Load Data
    df = load_data(raw_data_path)
    
    # 2. Basic validation
    basic_validation(df)
    
    # 3. Save as intermediate processed (optional, but good for pipeline)
    os.makedirs('data/processed', exist_ok=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype(str)
    df['StockCode'] = df['StockCode'].astype(str)
    df['Description'] = df['Description'].astype(str)
    out_path = 'data/processed/01_loaded.parquet'
    df.to_parquet(out_path, index=False)
    print(f"\nData saved to {out_path}")
