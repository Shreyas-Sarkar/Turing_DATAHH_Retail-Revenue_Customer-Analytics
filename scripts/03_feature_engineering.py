import pandas as pd
import numpy as np
import os

def engineer_features(df):
    print("Initial shape:", df.shape)
    
    # 1. Revenue
    # Revenue = Quantity * UnitPrice. For returns, this will be negative, which correctly deducts from total revenue.
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    # 2. Time-based features
    # Ensure InvoiceDate is datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Weekday'] = df['InvoiceDate'].dt.day_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    
    # 3. Categorizing Countries (Domestic vs International)
    # The dataset is UK-based, so UK is domestic.
    df['IsDomestic'] = df['Country'].apply(lambda x: True if x == 'United Kingdom' else False)
    
    print("Features engineered successfully.")
    print("Final shape:", df.shape)
    return df

if __name__ == "__main__":
    in_path = 'data/processed/02_cleaned.parquet'
    df = pd.read_parquet(in_path)
    
    df_engineered = engineer_features(df)
    
    out_path = 'data/processed/03_engineered.parquet'
    df_engineered.to_parquet(out_path, index=False)
    
    # Save a CSV version for Tableau to easily consume
    tableau_path = 'data/processed/tableau_export.csv'
    df_engineered.to_csv(tableau_path, index=False)
    
    print(f"\nEngineered data saved to {out_path} and {tableau_path}")
