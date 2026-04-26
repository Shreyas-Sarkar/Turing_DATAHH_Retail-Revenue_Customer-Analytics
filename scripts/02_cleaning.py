import pandas as pd
import numpy as np
import os

def clean_data(df):
    print("Initial shape:", df.shape)
    
    # 1. Drop duplicate rows
    df = df.drop_duplicates()
    print("Shape after dropping duplicates:", df.shape)
    
    # 2. Handle missing CustomerID
    # Since this is an analytics project tracking customer behavior, 
    # dropping rows with missing CustomerID is standard as we can't tie them to a user.
    # We will log how many we drop.
    missing_cust = df['CustomerID'].isnull().sum()
    print(f"Dropping {missing_cust} rows with missing CustomerID.")
    df = df.dropna(subset=['CustomerID'])
    
    # Convert CustomerID to integer to remove decimal points, then to string for categorical treatment
    df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
    
    # 3. Handle Returns and Quantity
    # Returns are identified by negative quantity and InvoiceNo starting with 'C'
    # We will keep them but flag them.
    df['IsReturn'] = df['InvoiceNo'].astype(str).str.startswith('C')
    
    # Ensure all returns have negative quantity, and vice versa
    # For now, we just validate:
    anomalous_returns = df[(df['IsReturn']) & (df['Quantity'] > 0)]
    if not anomalous_returns.empty:
        print(f"Warning: Found {len(anomalous_returns)} return invoices with positive quantity.")
    
    anomalous_qty = df[(~df['IsReturn']) & (df['Quantity'] < 0)]
    if not anomalous_qty.empty:
        print(f"Warning: Found {len(anomalous_qty)} non-return invoices with negative quantity.")
        
    # We'll drop rows where Quantity is 0 or negative but NOT a return (if any) or just drop Quantity = 0
    df = df[df['Quantity'] != 0]
    
    # 4. Handle Invalid Prices
    # UnitPrice should be > 0.
    invalid_prices = df[df['UnitPrice'] <= 0]
    print(f"Dropping {len(invalid_prices)} rows with UnitPrice <= 0.")
    df = df[df['UnitPrice'] > 0]
    
    # 5. Handle Description
    df['Description'] = df['Description'].str.strip()
    # Drop rows with empty description
    df = df.dropna(subset=['Description'])
    
    print("Shape after cleaning:", df.shape)
    return df

if __name__ == "__main__":
    in_path = 'data/processed/01_loaded.parquet'
    df = pd.read_parquet(in_path)
    
    df_clean = clean_data(df)
    
    out_path = 'data/processed/02_cleaned.parquet'
    df_clean.to_parquet(out_path, index=False)
    print(f"\nCleaned data saved to {out_path}")
