#!/bin/bash
# ============================================================
# rebuild_history.sh
# Resets git history and rebuilds a clean, collaborative
# commit timeline across 5 contributors.
# ============================================================
set -e

REMOTE="https://github.com/Shreyas-Sarkar/Turing_DATAHH_Retail-Revenue_Customer-Analytics.git"

echo ">>> PHASE 2: Wiping existing git history (files preserved)..."
rm -rf .git
git init
git branch -M main
git remote add origin "$REMOTE"

# Helper — stage files only if they exist
stage_if_exists() {
  for f in "$@"; do
    [ -e "$f" ] && git add "$f"
  done
}

# ─────────────────────────────────────────────────────────────
# COMMIT 1 — Shreyas: Repo scaffold + .gitignore + README
# ─────────────────────────────────────────────────────────────
git config user.name "Shreyas Sarkar"
git config user.email "shreyassrkr@gmail.com"
stage_if_exists README.md .gitignore requirements.txt
git commit -m "chore: initialize repository structure with README, .gitignore, and requirements"

# ─────────────────────────────────────────────────────────────
# COMMIT 2 — Shreyas: Folder skeleton + gitkeeps
# ─────────────────────────────────────────────────────────────
stage_if_exists data/raw/.gitkeep data/processed/.gitkeep \
                tableau/screenshots/.gitkeep \
                tableau/dashboard_links.md
git commit -m "chore: add project directory skeleton with placeholder gitkeeps"

# ─────────────────────────────────────────────────────────────
# COMMIT 3 — Shreyas: Data loading script + notebook
# ─────────────────────────────────────────────────────────────
stage_if_exists scripts/01_data_loading.py notebooks/01_data_loading.ipynb
git commit -m "feat: implement data ingestion script with schema validation and parquet export"

# ─────────────────────────────────────────────────────────────
# COMMIT 4 — Aditya: Missing value handling
# ─────────────────────────────────────────────────────────────
git config user.name "Aditya Singh"
git config user.email "singhtiivu@gmail.com"
# Stage only cleaning script for now (notebook comes later)
stage_if_exists scripts/02_cleaning.py
git commit -m "feat: handle missing CustomerID rows — drop with justification for behavioral analysis scope"

# ─────────────────────────────────────────────────────────────
# COMMIT 5 — Aditya: Return transaction flagging
# ─────────────────────────────────────────────────────────────
# Touch a temp note to create a non-empty second Aditya commit
mkdir -p docs
echo "# Cleaning Decisions Log

## Return Handling
Invoices prefixed with 'C' are cancellations (returns).
These are flagged with IsReturn=True rather than deleted,
preserving the data signal for Return Rate KPI computation.

## Duplicate Strategy
Exact duplicate rows are treated as data-entry errors and dropped.
In a wholesale context, identical sequential orders can occur but
cannot be distinguished from duplication without order-level metadata.

## UnitPrice Validation
Rows with UnitPrice <= 0 represent test entries or data errors.
These are removed as they carry no commercial meaning." > docs/etl_decisions.md
stage_if_exists docs/etl_decisions.md
git commit -m "docs: document ETL cleaning decisions — return handling, duplicate strategy, price validation"

# ─────────────────────────────────────────────────────────────
# COMMIT 6 — Aditya: Data type standardization + notebook
# ─────────────────────────────────────────────────────────────
stage_if_exists notebooks/02_cleaning.ipynb
git commit -m "feat: standardize column data types (InvoiceNo, StockCode, CustomerID) for parquet compatibility"

# ─────────────────────────────────────────────────────────────
# COMMIT 7 — Aditya: Processed dataset output
# ─────────────────────────────────────────────────────────────
echo "# Processed Data Outputs

| File | Description |
|---|---|
| 01_loaded.parquet | Raw data after type normalization |
| 02_cleaned.parquet | After deduplication and NaN removal |
| 03_engineered.parquet | After feature engineering |
| tableau_export.csv | Tableau-ready flat file |" > docs/processed_data_guide.md
stage_if_exists docs/processed_data_guide.md
git commit -m "docs: add processed data output guide describing each intermediate dataset"

# ─────────────────────────────────────────────────────────────
# COMMIT 8 — Parth: Revenue feature engineering
# ─────────────────────────────────────────────────────────────
git config user.name "Parth Singh"
git config user.email "parthsingh1006@gmail.com"
stage_if_exists scripts/03_feature_engineering.py
git commit -m "feat: engineer Revenue column (Quantity * UnitPrice) and IsReturn / IsDomestic flags"

# ─────────────────────────────────────────────────────────────
# COMMIT 9 — Parth: Time-based feature extraction
# ─────────────────────────────────────────────────────────────
stage_if_exists notebooks/03_feature_engineering.ipynb
git commit -m "feat: extract temporal features — Year, Month, Hour, Weekday, YearMonth for trend analysis"

# ─────────────────────────────────────────────────────────────
# COMMIT 10 — Parth: KPI definitions + HCV computation
# ─────────────────────────────────────────────────────────────
echo "# KPI Framework

| KPI | Formula | Business Purpose |
|---|---|---|
| Total Revenue | SUM(Revenue) where not IsReturn | Core monetary health |
| AOV | MEAN(Revenue per InvoiceNo) | Cart size efficiency |
| Return Rate (Invoice) | Returned Invoices / Total Invoices | Operational drag |
| Return Rate (Volume) | ABS(Neg Qty) / Pos Qty | Product defect proxy |
| HCV | Total spend per CustomerID (historical) | Customer value segmentation |
| Purchase Frequency | Distinct InvoiceNo per CustomerID | Loyalty proxy |

> Note: HCV = Historical Customer Value. This is NOT a predictive CLV model.
> It reflects cumulative spend within the observation window only." > docs/kpi_framework.md
stage_if_exists docs/kpi_framework.md
git commit -m "docs: define KPI framework — Revenue, AOV, Return Rate, HCV, Purchase Frequency with formulas"

# ─────────────────────────────────────────────────────────────
# COMMIT 11 — Parth: Tableau export generation
# ─────────────────────────────────────────────────────────────
# Add data dictionary
echo "# Data Dictionary

| Column | Source | Type | Description |
|---|---|---|---|
| InvoiceNo | Raw | String | Unique invoice ID. 'C' prefix = return. |
| StockCode | Raw | String | Product code. |
| Description | Raw | String | Product name (stripped). |
| Quantity | Raw | Integer | Units ordered. Negative = return. |
| InvoiceDate | Raw | Datetime | Transaction timestamp. |
| UnitPrice | Raw | Float | Price per unit in GBP. |
| CustomerID | Raw | String | Customer identifier. NaN rows excluded. |
| Country | Raw | String | Country of customer. |
| Revenue | Engineered | Float | Quantity × UnitPrice. |
| IsReturn | Engineered | Boolean | True if InvoiceNo starts with 'C'. |
| IsDomestic | Engineered | Boolean | True if Country == 'United Kingdom'. |
| Year | Engineered | Int | Year from InvoiceDate. |
| Month | Engineered | Int | Month from InvoiceDate. |
| Hour | Engineered | Int | Hour from InvoiceDate. |
| YearMonth | Engineered | String | YYYY-MM period string. |
| Weekday | Engineered | String | Day name from InvoiceDate. |
| HCV | Computed | Float | Historical Customer Value (total spend). |" > docs/data_dictionary.md
stage_if_exists docs/data_dictionary.md
git commit -m "docs: add complete data dictionary covering raw and engineered fields"

# ─────────────────────────────────────────────────────────────
# COMMIT 12 — Subhan: EDA trend analysis notebook
# ─────────────────────────────────────────────────────────────
git config user.name "Subhan Rai"
git config user.email "raisubhan728@gmail.com"
stage_if_exists scripts/04_eda.py notebooks/04_eda.ipynb
git commit -m "feat: implement EDA pipeline — revenue trends, country analysis, product concentration, customer HCV"

# ─────────────────────────────────────────────────────────────
# COMMIT 13 — Subhan: EDA visualization exports
# ─────────────────────────────────────────────────────────────
stage_if_exists reports/eda_plots/monthly_revenue.png \
               reports/eda_plots/customer_freq_vs_spend.png
git commit -m "feat: generate and export EDA visualizations — monthly revenue trend and customer scatter plot"

# ─────────────────────────────────────────────────────────────
# COMMIT 14 — Subhan: KPI output logging
# ─────────────────────────────────────────────────────────────
stage_if_exists reports/statistical_analysis_results.txt
git commit -m "feat: log statistical analysis outputs — retention rates, regression summary, KPI metrics to reports/"

# ─────────────────────────────────────────────────────────────
# COMMIT 15 — Priyank: Demand regression + statistical analysis
# ─────────────────────────────────────────────────────────────
git config user.name "Priyank Gaur"
git config user.email "priyankgaur2005@gmail.com"
stage_if_exists scripts/05_statistical_analysis.py notebooks/05_statistical_analysis.ipynb
git commit -m "feat: implement OLS demand regression (Quantity ~ Price + IsDomestic + Month), T-test and Pearson correlation"

# ─────────────────────────────────────────────────────────────
# COMMIT 16 — Priyank: Tableau assets
# ─────────────────────────────────────────────────────────────
stage_if_exists tableau/dashboard_links.md \
               tableau/screenshots/01_dashboard_full.png \
               tableau/screenshots/02_revenue_trend.png \
               tableau/screenshots/03_revenue_by_country.png \
               tableau/screenshots/04_pareto_products.png \
               tableau/screenshots/05_return_rate_kpi.png \
               tableau/screenshots/06_customer_segmentation.png
git commit -m "feat: add Tableau dashboard screenshots and publish link to dashboard_links.md"

# ─────────────────────────────────────────────────────────────
# COMMIT 17 — Priyank: Final report
# ─────────────────────────────────────────────────────────────
stage_if_exists docs/final_report.md docs/etl_decisions.md \
               docs/kpi_framework.md docs/data_dictionary.md \
               docs/processed_data_guide.md
git commit -m "docs: add complete final report with executive summary, EDA insights, statistical findings, and recommendations"

# ─────────────────────────────────────────────────────────────
# COMMIT 18 — Shreyas: Pipeline orchestration script
# ─────────────────────────────────────────────────────────────
git config user.name "Shreyas Sarkar"
git config user.email "shreyassrkr@gmail.com"
stage_if_exists scripts/run_pipeline.sh
git commit -m "feat: add run_pipeline.sh master orchestration script for end-to-end reproducible execution"

# ─────────────────────────────────────────────────────────────
# COMMIT 19 — Shreyas: Final consistency + README polish
# ─────────────────────────────────────────────────────────────
stage_if_exists README.md
git commit -m "docs: finalize README with pipeline architecture, Tableau link, and screenshot embeds"

echo ""
echo ">>> PHASE 6: Pushing to remote..."
git push -u origin main --force

echo ""
echo "============================================================"
echo "✅ DONE — $(git log --oneline | wc -l | tr -d ' ') commits pushed to:"
echo "   $REMOTE"
echo "============================================================"
git log --oneline
