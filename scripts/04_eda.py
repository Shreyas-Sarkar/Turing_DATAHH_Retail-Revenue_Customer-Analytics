import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(df, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    
    print("--- 1. Revenue Trends Over Time ---")
    monthly_rev = df.groupby('YearMonth')['Revenue'].sum().reset_index()
    monthly_rev = monthly_rev.sort_values('YearMonth')
    plt.figure(figsize=(10,6))
    sns.barplot(data=monthly_rev, x='YearMonth', y='Revenue')
    plt.xticks(rotation=45)
    plt.title('Monthly Revenue')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'monthly_revenue.png'))
    plt.close()
    
    print("--- 2. Product Level Distribution (Top SKUs) ---")
    top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)
    print("Top 10 Products by Revenue:\n", top_products)
    
    print("\n--- 3. Country-wise Sales Distribution ---")
    country_rev = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)
    print("Top 10 Countries by Revenue:\n", country_rev)
    
    print("\n--- 4. Customer Behavior & Historical Customer Value (HCV) ---")
    customer_stats = df.groupby('CustomerID').agg({
        'InvoiceNo': 'nunique', # Frequency
        'Revenue': 'sum'        # Monetary
    }).rename(columns={'InvoiceNo': 'PurchaseFrequency', 'Revenue': 'TotalSpend'})
    
    # Calculate HCV (Average spend per purchase * Purchase frequency)
    # This mathematically equals TotalSpend. We use HCV instead of CLV as it is non-predictive.
    customer_stats['HCV'] = customer_stats['TotalSpend']
    
    print(customer_stats.describe())
    
    print("\n--- 5. KPI Computations ---")
    total_revenue = df['Revenue'].sum()
    print(f"Total Valid Revenue: £{total_revenue:.2f}")
    
    # Return Rate (% of invoices that are returns)
    total_invoices = df['InvoiceNo'].nunique()
    return_invoices = df[df['IsReturn']]['InvoiceNo'].nunique()
    return_rate_invoices = (return_invoices / total_invoices) * 100
    
    # Return Volume Rate (% of negative quantity relative to total absolute quantity)
    neg_qty = abs(df[df['Quantity'] < 0]['Quantity'].sum())
    pos_qty = df[df['Quantity'] > 0]['Quantity'].sum()
    return_rate_qty = (neg_qty / pos_qty) * 100 if pos_qty > 0 else 0
    
    print(f"Return Rate (by Invoice): {return_rate_invoices:.2f}%")
    print(f"Return Rate (by Volume): {return_rate_qty:.2f}%")
    
    # Plotting Frequency vs Spend
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=customer_stats, x='PurchaseFrequency', y='TotalSpend', alpha=0.5)
    plt.title('Customer Frequency vs Total Spend')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'customer_freq_vs_spend.png'))
    plt.close()

if __name__ == "__main__":
    in_path = 'data/processed/03_engineered.parquet'
    df = pd.read_parquet(in_path)
    
    run_eda(df, 'reports/eda_plots')
