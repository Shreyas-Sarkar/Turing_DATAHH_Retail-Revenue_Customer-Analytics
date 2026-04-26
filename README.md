# Capstone Project 2: UK Online Retail Analytics

## 1. Project Overview & Problem Statement
This repository contains an end-to-end data analytics pipeline analyzing transactional data from a UK-based online retail store. The primary business problem is to identify underlying revenue drivers, map customer purchasing behavior, and isolate operational bottlenecks (like return rates) to provide targeted, decision-oriented business recommendations.

The project demonstrates a production-grade ETL architecture, rigorous exploratory data analysis, statistical demand forecasting, and an interactive decision-support Tableau dashboard.

## 2. Dataset Description
- **Source**: UK Online Retail Dataset (UCI Machine Learning Repository)
- **Size**: ~500,000 rows, 8 columns
- **Features**: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`.
- **Note**: The original dataset in `data/raw/` is kept immutable. All transformations handle anomalies (e.g., negative quantities for returns), missing data (dropped missing `CustomerID` rows for behavioral clustering), and output to `data/processed/`.

## 3. Pipeline Architecture
Our analytical pipeline follows a strict, reproducible workflow:
1. **ETL Processing (`scripts/01_data_loading.py` to `03_feature_engineering.py`)**: Cleans data, engineers time-based features, and exports a Tableau-ready `.csv`.
2. **Exploratory Data Analysis (`scripts/04_eda.py`)**: Computes core KPIs including Return Rates and Historical Customer Value (HCV). Generates visualizations in `reports/eda_plots/`.
3. **Statistical Analysis (`scripts/05_statistical_analysis.py`)**: Validates hypotheses (e.g., AOV differences via T-Tests) and runs an OLS Multivariate Regression targeting **Demand (`Quantity`)** to prove price elasticity.
4. **Jupyter Notebook Generation**: The pipeline automatically compiles all scripts into reproducible Jupyter Notebooks (`.ipynb`) using `jupytext`.

## 4. Repository Structure
```
dva/
├── data/
│   ├── raw/                 # Unchanged, original raw data
│   └── processed/           # Cleaned and engineered datasets (.parquet & .csv)
├── docs/                    
│   └── final_report.md      # Comprehensive findings and business recommendations
├── notebooks/               # Auto-generated reproducible Jupyter Notebooks
├── reports/                 # Output text summaries and EDA plots
├── scripts/                 # Modular Python pipeline scripts
│   └── run_pipeline.sh      # Master execution script
└── tableau/
    ├── dashboard_links.md   # Link to Tableau Public
    └── screenshots/         # Dashboard visual evidence
```

## 5. How to Run the Pipeline
1. Set up a Python environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Execute the fully automated bash script, which processes data and builds the notebooks:
   ```bash
   chmod +x scripts/run_pipeline.sh
   ./scripts/run_pipeline.sh
   ```

## 6. Tableau Dashboard
An interactive dashboard was constructed to allow stakeholders to drill down dynamically into Revenue Drivers, Product Performance, and Customer Segments. 

**[🔗 View the Interactive Dashboard on Tableau Public](https://public.tableau.com/views/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)** *(Link available in `tableau/dashboard_links.md`)*

### Dashboard Previews
> **Note:** Manual screenshot population is required prior to final submission. Place images in `tableau/screenshots/`.
- ![Full Dashboard](tableau/screenshots/dashboard_full.png)
- ![Revenue Trend](tableau/screenshots/dashboard_revenue_trend.png)
- ![Revenue by Country](tableau/screenshots/dashboard_revenue_country.png)
- ![Pareto Products](tableau/screenshots/dashboard_pareto.png)
- ![Return Rate KPI](tableau/screenshots/dashboard_return_rate.png)
- ![Customer Segmentation](tableau/screenshots/dashboard_customer_segmentation.png)

---
*Created for Industry Capstone Project 2. This repository evaluates Registered Customer behavior strictly.*
