# NST DVA Capstone 2 - Project Repository
---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | UK Online Retail Analytics: Revenue Drivers, Return Behaviour and Customer Insights |
| **Sector** | E-Commerce / Online Retail |
| **Institute** | Newton School of Technology |
| **Submission Date** | 27 Apr 2026 |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Shreyas Sarkar | Shreyas-Sarkar |
| Data Lead | Shreyas Sarkar | _TBD_ |
| ETL Lead | Aditya Singh | _TBD_ |
| Analysis Lead | Subhan Rai | _TBD_ |
| Visualization Lead | Priyank Gaur | _TBD_ |
| Strategy Lead | Parth Singh | _TBD_ |


---

## Business Problem

A UK-based online retailer needs a clearer view of what drives revenue, where returns are creating operational loss, and which customer segments contribute the most value. The project supports business stakeholders in pricing, operations, and inventory planning by combining ETL, KPI tracking, statistical testing, and dashboarding. The key challenge is converting noisy transactional data into decision-ready insights with reproducible logic.

**Core Business Question**

> Which products, customer segments, geographies, and time periods should the business prioritize to increase revenue while reducing return-driven leakage?

**Decision Supported**

> This analysis supports decisions on international growth strategy, seasonal inventory planning, return-reduction interventions, and high-value customer retention programs.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | UCI Machine Learning Repository (Online Retail Dataset) |
| **Direct Access Link** | https://archive.ics.uci.edu/ml/datasets/Online+Retail |
| **Row Count** | 541,909 raw rows (401,564 cleaned rows used in analysis) |
| **Column Count** | 8 raw columns (16 columns after feature engineering) |
| **Time Period Covered** | 01 Dec 2010 to 09 Dec 2011 |
| **Format** | Excel (.xlsx) |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| InvoiceNo | Unique invoice ID; `C` prefix denotes cancellations/returns | Return identification and invoice-level KPIs |
| Quantity | Transaction line quantity (negative for returns) | Demand, return volume, revenue computation |
| UnitPrice | Per-unit price in GBP | AOV, price-demand relationship, regression |
| CustomerID | Registered customer identifier | Customer segmentation, HCV, retention analysis |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| Total Revenue (Registered) | Revenue generated from non-return registered-customer transactions | `SUM(Revenue) where IsReturn == False` |
| Average Order Value (AOV) | Average invoice value | `mean(invoice_revenue by InvoiceNo)` |
| Return Rate (Invoice) | Share of invoices that are returns | `returned_invoices / total_invoices` |
| Historical Customer Value (HCV) | Historical spend concentration across customers | `sum(Revenue) by CustomerID` |

Current benchmark values from analysis outputs:
- Total Revenue: £8,278,519.42
- AOV: £479.56
- Domestic AOV: £437.64
- International AOV: £849.51
- Return Rate (Invoice): 16.47%
- Return Rate (Volume): 5.30%

Documented KPI logic: `scripts/04_eda.py`, `docs/kpi_framework.md`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | https://public.tableau.com/views/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights?:language=en-GB&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link |
| **Executive View** | KPI header with Total Revenue, AOV, Return Rate and high-level trend/context visuals |
| **Operational View** | Drill-down into revenue by country, top product concentration, and customer-value behavior |
| **Main Filters** | Date (Year/Month), Country, Product/SKU |

Screenshots are stored in [`tableau/screenshots/`](tableau/screenshots/) and dashboard links are documented in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. Revenue shows strong seasonality, rising sharply in Sep-Nov and peaking at about £1.13M in Nov 2011.
2. International AOV (£849.51) is almost double domestic AOV (£437.64), indicating stronger order consolidation abroad.
3. UK drives the majority of revenue (~81.5%), but non-UK orders are more efficient at invoice level.
4. Return pressure is material: 16.47% of invoices are return transactions.
5. Return volume rate is lower (5.3%) than return invoice rate, suggesting many small-item returns rather than large reversals.
6. Product concentration risk exists: a few SKUs drive a disproportionate share of revenue.
7. HCV is highly right-skewed (mean far above median), indicating a small high-value customer cohort.
8. Statistical tests confirm a significant domestic vs international AOV difference (p-value ~9.29e-22).
9. Regression shows price has a statistically significant negative relationship with demand quantity.
10. Month-over-month retention falls to 22.3% in Dec, indicating a post-peak retention gap.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | International AOV is 94% higher than domestic | Apply country-targeted campaigns and minimum-order shipping thresholds for key non-UK markets | +£250K to +£300K annual incremental revenue potential |
| 2 | Revenue concentration is strongly seasonal in Q4 | Pre-stage inventory/logistics before Q4 and run Q2 demand-generation campaigns | Better fulfillment reliability and reduced peak operational stress |
| 3 | Return invoice rate is high (16.47%) | Run SKU-level QA and labeling checks on top returned products | Reduced return leakage and improved customer experience |
| 4 | HCV is concentrated in a small customer tier | Launch tiered VIP retention program for high-HCV customers | Higher retention and protected recurring high-value revenue |

---

## Repository Structure

```text
Turing_DATAHH_Retail-Revenue_Customer-Analytics/
|
|-- README.md
|-- requirements.txt
|
|-- data/
|   |-- raw/
|   `-- processed/
|
|-- docs/
|   |-- data_dictionary.md
|   |-- etl_decisions.md
|   |-- final_report.md
|   |-- kpi_framework.md
|   `-- processed_data_guide.md
|
|-- notebooks/
|   |-- 01_data_loading.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_feature_engineering.ipynb
|   |-- 04_eda.ipynb
|   `-- 05_statistical_analysis.ipynb
|
|-- scripts/
|   |-- 01_data_loading.py
|   |-- 02_cleaning.py
|   |-- 03_feature_engineering.py
|   |-- 04_eda.py
|   |-- 05_statistical_analysis.py
|   `-- run_pipeline.sh
|
|-- reports/
|   |-- statistical_analysis_results.txt
|   `-- eda_plots/
|
`-- tableau/
    |-- dashboard_links.md
    `-- screenshots/
```

---

## Analytical Pipeline

The project follows a structured workflow:

1. **Define** - Business problem and stakeholder-focused decision context were documented.
2. **Extract** - Data ingestion implemented in `scripts/01_data_loading.py`.
3. **Clean and Transform** - Cleaning and validation in `scripts/02_cleaning.py`.
4. **Feature Engineering** - Revenue, return, geography, and temporal features in `scripts/03_feature_engineering.py`.
5. **Analyze** - EDA and KPI computation in `scripts/04_eda.py`.
6. **Statistical Validate** - Correlation, t-test, retention, and OLS regression in `scripts/05_statistical_analysis.py`.
7. **Visualize and Report** - Tableau dashboard plus report artifacts in `docs/`, `reports/`, and `tableau/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Libraries used:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `pyarrow`, `jupytext`

---

## Submission Checklist

**GitHub Repository**

- [✅] Public repository created with the correct naming convention (`SectionName_TeamID_ProjectName`)
- [✅] All notebooks committed in `.ipynb` format
- [✅] `data/raw/` contains the original, unedited dataset
- [✅] `data/processed/` contains the cleaned pipeline output
- [✅] `tableau/screenshots/` contains dashboard screenshots
- [✅] `tableau/dashboard_links.md` contains the Tableau Public URL
- [✅] `docs/data_dictionary.md` is complete
- [✅] `README.md` explains the project, dataset, and team
- [✅]  All members have visible commits and pull requests

**Tableau Dashboard**

- [✅] Published on Tableau Public and accessible via public URL
- [✅] At least one interactive filter included
- [✅] Dashboard directly addresses the business problem

**Project Report**

- [✅] Final report exported as PDF into `reports/`
- [✅] Cover page, executive summary, sector context, problem statement
- [✅] Data description, cleaning methodology, KPI framework
- [✅] EDA with written insights, statistical analysis results
- [✅] Dashboard screenshots and explanation
- [✅] 8-12 key insights in decision language
- [✅] 3-5 actionable recommendations with impact estimates
- [✅] Contribution matrix matches GitHub history

**Presentation Deck**

- [✅] Final presentation exported as PDF into `reports/`
- [✅] Title slide through recommendations, impact, limitations, and next steps

**Individual Assets**

- [✅] DVA-oriented resume updated to include this capstone
- [✅] Portfolio link or project case study added

---

## Contribution Matrix

This table is mapped from commit history and changed-file ownership in this repository.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| Shreyas Sarkar | Owner | Support | Support | Support | Support | Support | Support |
| Aditya Singh | Support | Owner | Support | Support | Support | Support | Support |
| Parth Singh | Support | Support | Support | Support | Support | Owner | Support |
| Subhan Rai | Support | Support | Owner | Owner | Support | Support | Support |
| Priyank Gaur | Support | Support | Support | Owner | Owner | Owner | Support |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** Aditya Singh

**Date:** 27/04/2026

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
