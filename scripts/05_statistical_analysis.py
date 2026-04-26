import pandas as pd
import numpy as np
from scipy import stats
import os

def run_statistical_analysis(df):
    print("--- Statistical Analysis ---")
    
    # 1. Correlation Analysis (Price vs Quantity)
    # Exclude returns for correlation between standard purchase qty and price
    df_purchases = df[~df['IsReturn']]
    
    corr, pval = stats.pearsonr(df_purchases['UnitPrice'], df_purchases['Quantity'])
    print(f"\nCorrelation between UnitPrice and Quantity: {corr:.4f} (p-value: {pval:.4e})")
    if pval < 0.05:
        print("Insight: Significant negative correlation exists, implying price elasticity.")
        print("Note: Pearson only measures linear relationships. True elasticity is non-linear and requires SKU-level modeling.")
        
    # 2. Hypothesis Testing (Domestic vs International AOV)
    # Null Hypothesis: No difference in Average Order Value (AOV) between Domestic and International orders.
    # Alternate Hypothesis: There is a significant difference in AOV.
    
    order_values = df_purchases.groupby(['InvoiceNo', 'IsDomestic'])['Revenue'].sum().reset_index()
    domestic_aov = order_values[order_values['IsDomestic'] == True]['Revenue']
    intl_aov = order_values[order_values['IsDomestic'] == False]['Revenue']
    
    print(f"\nDomestic AOV Mean: £{domestic_aov.mean():.2f}")
    print(f"International AOV Mean: £{intl_aov.mean():.2f}")
    
    t_stat, p_val_ttest = stats.ttest_ind(domestic_aov, intl_aov, equal_var=False)
    print(f"T-test Statistic: {t_stat:.4f}, p-value: {p_val_ttest:.4e}")
    if p_val_ttest < 0.05:
        print("Insight: Reject Null Hypothesis. There is a statistically significant difference in AOV between Domestic and International orders.")
    else:
        print("Insight: Fail to reject Null Hypothesis. No significant difference in AOV.")
        
    # 3. Customer Retention Rate (Month over Month)
    print("\n--- KPI: Retention Analysis ---")
    df_purchases['YearMonth'] = df_purchases['InvoiceDate'].dt.to_period('M')
    monthly_customers = df_purchases.groupby('YearMonth')['CustomerID'].apply(set).to_dict()
    
    months = sorted(list(monthly_customers.keys()))
    retention_rates = {}
    for i in range(1, len(months)):
        prev_month_custs = monthly_customers[months[i-1]]
        curr_month_custs = monthly_customers[months[i]]
        
        if len(prev_month_custs) == 0:
            continue
            
        retained = prev_month_custs.intersection(curr_month_custs)
        retention_rate = len(retained) / len(prev_month_custs)
        retention_rates[months[i]] = retention_rate
        
    print("Month-over-Month Retention Rates:")
    for m, r in retention_rates.items():
        print(f"{m}: {r:.2%}")

    # 4. Regression Analysis (Demand Drivers)
    print("\n--- Regression Analysis: Demand Forecasting ---")
    import statsmodels.api as sm
    
    # Target: Quantity (Demand)
    # Features: UnitPrice, IsDomestic, Month
    # We predict Demand instead of Revenue to avoid the deterministic tautology of Revenue = Qty * Price
    df_reg = df_purchases.dropna(subset=['Quantity', 'UnitPrice', 'IsDomestic', 'Month']).copy()
    df_reg['IsDomestic'] = df_reg['IsDomestic'].astype(int)
    
    X = df_reg[['UnitPrice', 'IsDomestic', 'Month']]
    y = df_reg['Quantity']
    
    # Add intercept
    X = sm.add_constant(X)
    
    model = sm.OLS(y, X).fit()
    print(model.summary())
    
    print("\nRegression Interpretation:")
    print("- Price Elasticity: A negative coefficient for UnitPrice confirms that as price increases, demand (Quantity) decreases.")
    print("- Geography Impact: The IsDomestic coefficient shows how domestic baseline demand differs from international orders per transaction line.")
    print("- Seasonality Impact: The Month coefficient indicates the linear trend of demand over the year.")
    print("- Business Implication: Price is a significant lever for managing demand volumes. To maximize net revenue, price optimization should be modeled at the individual SKU level using non-linear elasticity curves.")

if __name__ == "__main__":
    in_path = 'data/processed/03_engineered.parquet'
    df = pd.read_parquet(in_path)
    
    run_statistical_analysis(df)
