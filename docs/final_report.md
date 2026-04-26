# Capstone Project 2: UK Online Retail Analytics
## Final Report

---

**Project Title:** UK Online Retail Analytics: Revenue Drivers, Return Behaviour & Customer Insights

**Sector:** E-Commerce / Online Retail

**Institute:** Newton School of Technology

**Dataset:** UCI Machine Learning Repository – Online Retail Dataset

**GitHub Repository:** https://github.com/

**Tableau Public Dashboard:** https://public.tableau.com/views/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights

**Date:** April 2026

---

## 1. Executive Summary

A UK-based online retailer needed to understand what was driving revenue volatility, which customers represented the highest value, and where operational losses (in the form of returns) were creating hidden costs. This project delivers answers to all three.

Using a Python-based ETL pipeline and an interactive Tableau dashboard built on ~400,000 cleaned transactional records, the analysis revealed:

- **Extreme seasonality**: Revenue more than doubles between April and November, peaking at £1.13M in November 2011.
- **Geographic AOV gap**: International orders generate an average order value of £849.51 — nearly **double** the domestic AOV of £437.64 — presenting a clear expansion opportunity.
- **High return pressure**: 16.47% of all invoices are return transactions, creating operational drag that is not currently being managed strategically.
- **Product concentration risk**: A single product ("REGENCY CAKESTAND 3 TIER") alone generated £132,568 in revenue, exposing heavy catalog dependence.

**Key Recommendations:**
1. Introduce tiered minimum-order thresholds for international shipping to drive the already-high international AOV even further.
2. Invest marketing spend in Q2/Q3 to smooth Q4-driven revenue volatility and reduce seasonal operational risk.
3. Implement SKU-level return flagging to identify defective or mislabelled products before they reach customers.

---

## 2. Sector & Business Context

The UK online retail sector is characterised by high transaction volumes, diverse geographic reach, and a wholesale B2B customer base purchasing alongside individual consumers. Decision-makers in this space require:

- **Operations teams** to understand return volumes by product and region.
- **Pricing teams** to identify price-demand elasticity to optimise margins.
- **Supply chain teams** to plan inventory around predictable seasonal demand spikes.

This project directly serves these needs through a structured KPI framework and an interactive Tableau dashboard that allows stakeholders to filter by date, country, and product dynamically.

---

## 3. Problem Statement & Objectives

### Formal Problem Definition
The business lacks a consolidated, data-driven view of:
1. Which products, countries, and time periods drive the majority of revenue.
2. What the true operational cost of return transactions is.
3. Which customer segments hold the highest historical value and are candidates for targeted retention investment.

### Scope
**Included:**
- Registered customer transactions only (customers with valid CustomerID).
- Transactions spanning December 2010 to December 2011.
- Both domestic (UK) and international markets.

**Excluded:**
- Guest checkouts (missing CustomerID, ~25% of raw rows). This exclusion is an acknowledged bias — see Limitations.
- Transactions with UnitPrice ≤ 0 (zero-price test entries).

### Success Criteria
- A reproducible, automated ETL pipeline.
- A KPI framework computing revenue, return rates, purchase frequency, and Historical Customer Value (HCV).
- At least 8 decision-oriented, evidence-backed business insights.
- An interactive Tableau dashboard answering all three problem dimensions above.

---

## 4. Data Description

| Attribute | Value |
|---|---|
| Source | UCI Machine Learning Repository |
| Dataset Name | Online Retail |
| URL | https://archive.ics.uci.edu/ml/datasets/Online+Retail |
| Raw Rows | 541,909 |
| Columns | 8 |
| Time Period | 01 Dec 2010 – 09 Dec 2011 |
| Countries | 38 |
| Format | .xlsx |

### Column Descriptions

| Column | Type | Description |
|---|---|---|
| InvoiceNo | String | Unique invoice identifier. Prefix 'C' = cancellation/return. |
| StockCode | String | Product code. |
| Description | String | Product name. |
| Quantity | Integer | Units ordered. Negative for returns. |
| InvoiceDate | Datetime | Transaction timestamp. |
| UnitPrice | Float | Price per unit in GBP (£). |
| CustomerID | Float | Customer identifier. ~25% missing (guest checkouts). |
| Country | String | Country of the customer. |

### Data Bias Disclosure
Approximately 135,080 rows (24.9% of the raw dataset) were removed due to missing CustomerID values. These represent guest or untracked transactions and cannot be attributed to individual customer behaviour. All metrics in this report reflect **registered customers only** and will not perfectly reconcile with gross financial ledger totals.

---

## 5. Data Cleaning & ETL Pipeline

The ETL pipeline is built across three modular Python scripts, each outputting a validated intermediate Parquet file. The pipeline is fully automated via `scripts/run_pipeline.sh` and is deterministic on every run.

### Step 1: Data Loading (`01_data_loading.py`)
- Loaded `data/raw/Online Retail.xlsx` without modification.
- Standardised mixed-type columns (`InvoiceNo`, `StockCode`, `Description`) to string to prevent Parquet serialisation errors.
- Output: `data/processed/01_loaded.parquet` (541,909 rows, 8 columns).

### Step 2: Cleaning (`02_cleaning.py`)
| Transformation | Rows Affected | Justification |
|---|---|---|
| Drop duplicates | -5,268 rows | Exact duplicate records are data-entry errors. |
| Drop missing CustomerID | -135,037 rows | Cannot assign behaviour to anonymous transactions. |
| Drop UnitPrice ≤ 0 | -40 rows | Zero-price entries are test or error records. |
| Flag returns (IsReturn) | 8,872 invoices | Invoices starting with 'C' are returns; kept for Return Rate analysis. |
| Drop Quantity = 0 | ~0 rows | Zero-quantity rows carry no informational value. |
- Output: `data/processed/02_cleaned.parquet` (401,564 rows, 9 columns).

### Step 3: Feature Engineering (`03_feature_engineering.py`)
| Feature | Formula / Logic | Business Purpose |
|---|---|---|
| Revenue | Quantity × UnitPrice | Core monetary metric (negative for returns). |
| IsReturn | InvoiceNo.startswith('C') | Return flagging for KPI computation. |
| Year / Month / Hour | Extracted from InvoiceDate | Seasonality and time-of-day analysis. |
| YearMonth | Period string (YYYY-MM) | Monthly aggregation for trend analysis. |
| Weekday | Day name from InvoiceDate | Day-level purchasing pattern analysis. |
| IsDomestic | Country == 'United Kingdom' | Domestic vs. international segmentation. |
- Output: `data/processed/03_engineered.parquet` (401,564 rows, 16 columns) and `data/processed/tableau_export.csv`.

---

## 6. KPI Framework

All KPIs are computed directly from `03_engineered.parquet`. Formulas are defined in `scripts/04_eda.py`.

| KPI | Formula | Computed Value |
|---|---|---|
| Total Revenue (Registered) | Sum of Revenue where not IsReturn | £8,278,519.42 |
| Average Order Value (AOV) | Mean Revenue per InvoiceNo | £479.56 |
| Domestic AOV | Mean Revenue per invoice (UK only) | £437.64 |
| International AOV | Mean Revenue per invoice (non-UK) | £849.51 |
| Return Rate (Invoice) | Returned Invoices / Total Invoices | 16.47% |
| Return Rate (Volume) | Abs(Negative Qty) / Positive Qty | 5.30% |
| Unique Customers | Count of distinct CustomerIDs | 4,371 |
| Avg. Purchase Frequency | Mean invoices per customer | 5.08 |
| Historical Customer Value (HCV) | Total spend per customer (historical, non-predictive) | Mean: £1,894; Median: £644 |

> **Note on HCV:** Historical Customer Value (HCV) is a backward-looking metric representing total recorded spend per customer in the observation period. It is **not** a predictive Customer Lifetime Value (CLV) model.

---

## 7. Exploratory Data Analysis

### 7.1 Revenue Trends (Seasonality)

| Month | Revenue (£) |
|---|---|
| Dec 2010 | £552,373 |
| Jan 2011 | £473,732 |
| Feb 2011 | £435,534 |
| Mar 2011 | £578,576 |
| Apr 2011 | £425,223 |
| May 2011 | £647,012 |
| Jun 2011 | £606,863 |
| Jul 2011 | £573,112 |
| Aug 2011 | £615,078 |
| Sep 2011 | £929,356 |
| Oct 2011 | £973,306 |
| Nov 2011 | £1,126,815 |
| Dec 2011 (partial) | £341,539 |

**Observation:** Revenue escalates sharply from September onward, peaking at £1.13M in November 2011.
**Interpretation:** The business is heavily reliant on the pre-Christmas wholesale gifting cycle.
**Decision:** Inventory and staffing should be pre-scaled in August/September to avoid Q4 bottlenecks. Promotional spend in Q1–Q2 should be increased to smooth annual cash flow.

### 7.2 Geographic Distribution

| Country | Revenue (£) |
|---|---|
| United Kingdom | £6,747,156 |
| Netherlands | £284,662 |
| EIRE | £250,002 |
| Germany | £221,509 |
| France | £196,626 |
| Australia | £137,010 |

**Observation:** The UK contributes 81.5% of total revenue, yet international buyers spend almost twice as much per order (£849.51 vs. £437.64).
**Interpretation:** International buyers consolidate orders to offset shipping cost, which naturally inflates their basket size.
**Decision:** Introduce a minimum-order threshold (e.g., £500) for subsidised international shipping, pushing International AOV further without eroding margins.

### 7.3 Product Concentration

| Top Products | Revenue (£) |
|---|---|
| REGENCY CAKESTAND 3 TIER | £132,568 |
| WHITE HANGING HEART T-LIGHT HOLDER | £93,272 |
| JUMBO BAG RED RETROSPOT | £83,057 |
| PARTY BUNTING | £67,628 |
| POSTAGE | £66,710 |

**Observation:** The top 5 products alone contribute approximately £443K — over 5% of total registered-customer revenue.
**Interpretation:** The catalog exhibits strong Pareto concentration — a few products carry disproportionate revenue risk.
**Decision:** Introduce bundling strategies pairing top-selling items with slower-moving, complementary inventory to reduce catalog concentration risk and improve stock velocity.

### 7.4 Customer Behaviour (HCV Distribution)

| Metric | Value |
|---|---|
| Total Unique Customers | 4,371 |
| Mean HCV | £1,894 |
| Median HCV | £644 |
| Max HCV | £279,489 |
| Mean Purchase Frequency | 5.08 invoices |

**Observation:** The HCV distribution is highly right-skewed. The top-tier customers are worth orders of magnitude more than the median.
**Interpretation:** A small cohort of very high-frequency, high-spend customers drive a disproportionate share of total revenue.
**Decision:** Implement a tiered VIP programme targeting customers with HCV above £5,000, offering exclusive pricing or early access to new products to prevent churn in this critical segment.

---

## 8. Statistical Analysis

### 8.1 Pearson Correlation: Price vs. Demand

| Metric | Value |
|---|---|
| Pearson Correlation (r) | -0.0046 |
| p-value | 0.0041 |

**Result:** Statistically significant (p < 0.05). A negative correlation confirms that higher unit prices are associated with lower order quantities.

**Caveat:** Pearson measures only linear associations. This global correlation mixes all products across all price ranges. True price elasticity is non-linear and must be modelled at the individual SKU level. This result should be treated as directional evidence, not a precise elasticity coefficient.

---

### 8.2 T-Test: Domestic vs. International AOV

**Hypothesis:**
- H₀: There is no significant difference in Average Order Value between Domestic and International orders.
- H₁: A statistically significant difference in AOV exists between the two segments.

| Metric | Domestic (UK) | International |
|---|---|---|
| Mean AOV | £437.64 | £849.51 |
| T-Statistic | -9.6829 | — |
| p-value | 9.29e-22 | — |

**Result:** Null hypothesis rejected. The difference is statistically significant at the 99.999% confidence level. International buyers generate 94% higher order values on average.

**Business Implication:** The geographic pricing and shipping strategy is clearly bifurcated. International customers warrant a distinct operational strategy.

---

### 8.3 OLS Regression: Demand Forecasting

To identify demand drivers, an OLS regression was applied predicting **Quantity (Demand)** — not Revenue — to avoid the mathematical tautology inherent in predicting Revenue from its own multiplicative subcomponents (Quantity × UnitPrice).

**Model:** Quantity ~ const + UnitPrice + IsDomestic + Month

| Predictor | Coefficient | Std Error | t-Stat | p-value | Interpretation |
|---|---|---|---|---|---|
| Intercept | 22.53 | 1.065 | 21.14 | < 0.001 | Baseline demand per transaction line. |
| UnitPrice | -0.040 | 0.013 | -3.07 | 0.002 | Each £1 price increase reduces demand by 0.04 units per line. |
| IsDomestic | -8.79 | 0.918 | -9.58 | < 0.001 | Domestic transactions have ~9 fewer units per line than international. |
| Month | -0.19 | 0.084 | -2.28 | 0.022 | Slight linear demand decrease across calendar months. |

| Model Metric | Value |
|---|---|
| Observations | 392,692 |
| R-squared | 0.000 |
| F-statistic | 35.47 |
| Prob (F-stat) | 6.55e-23 |

**Important Limitation:** The R-squared of 0.00 indicates that the linear model explains virtually none of the variance in Quantity. This is expected given the extreme right-skew and heteroscedasticity of retail transaction data (Jarque-Bera statistic: 507 trillion). The F-statistic confirms the coefficients are collectively non-zero (i.e., statistically meaningful predictors exist), but the linear functional form is clearly misspecified for this distribution.

**Business Implication:** Price and geography are statistically significant demand levers, but SKU-level non-linear models are required for operationally actionable price optimisation.

---

## 9. Tableau Dashboard

The interactive Tableau dashboard is published at:

**[UK Retail Analytics Dashboard – Tableau Public](https://public.tableau.com/views/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights/UKRetailAnalyticsDashboardRevenueReturnsandCustomerInsights)**

### Dashboard Structure

| Sheet | Type | Business Question Answered |
|---|---|---|
| Revenue Trend | Line Chart | When does revenue peak? How does seasonality drive the business? |
| Revenue by Country | Bar / Map | Which markets drive volume vs. value? |
| Pareto (Top Products) | Bar + Line | Which SKUs are driving revenue concentration risk? |
| Return Rate KPI | Big Number | What is the operational drag from returns? |
| Customer Segmentation | Scatter Plot | Which customers are high-frequency, high-value and which are at-risk? |

### Interactivity
All charts support cross-filtering by Country and Date. Stakeholders can isolate performance for any country or time window with a single click.

---

## 10. Business Insights Summary

| # | Insight | Supporting Evidence | Decision |
|---|---|---|---|
| 1 | Revenue nearly triples from April to November | Monthly revenue table | Pre-scale inventory in Aug/Sep; increase off-season promotions |
| 2 | November is the single highest revenue month (£1.13M) | Monthly revenue table | Ensure stock and logistics readiness by October |
| 3 | International AOV is 94% higher than domestic | T-test, AOV table | Introduce international shipping minimum thresholds |
| 4 | UK generates 81.5% of revenue but at lower order efficiency | Country revenue table | Allocate growth marketing toward Netherlands, Germany |
| 5 | 16.47% of invoices are returns | KPI computation | Implement SKU-level QA flags for top-returned products |
| 6 | Return volume rate (5.3%) is low vs. invoice rate (16.47%) | KPI computation | Returns are frequent but small-quantity — likely defect-driven, not buyer's remorse |
| 7 | Top product ("REGENCY CAKESTAND") = £132,568 single-SKU dependency | Product revenue table | Bundle top sellers with slower-moving inventory |
| 8 | Median HCV (£644) is far below mean (£1,894) — extreme skew | HCV distribution table | A small VIP segment requires targeted retention investment |
| 9 | UnitPrice negatively predicts Quantity (coef: -0.04, p=0.002) | OLS Regression | Volume discounts on mid-tier products can increase basket sizes |
| 10 | IsDomestic has a -8.79 coefficient — international lines are larger | OLS Regression | International wholesale buyers need a distinct product catalogue and pricing tier |
| 11 | Retention rates drop to 22.3% in December | Retention computation | December is a drop-off month — post-holiday re-engagement campaigns needed |
| 12 | Mid-year monthly revenue averages £600K — no promotional spikes | Monthly revenue table | Mid-year promotional calendar is underdeveloped; flash sales can activate latent demand |

---

## 11. Recommendations

### R1: International Market Investment
**Insight:** International customers generate 94% higher AOV (£849.51 vs. £437.64).
**Action:** Establish country-specific marketing campaigns targeting Netherlands, Germany, and EIRE. Introduce minimum-order thresholds for subsidised international shipping (e.g., £500 minimum for free shipping).
**Estimated Impact:** Even a 10% increase in international order volume could add approximately £250,000–£300,000 in incremental annual revenue.

### R2: Seasonal Inventory & Promotional Planning
**Insight:** Revenue spikes from £425K (April) to £1.13M (November), creating extreme operational concentration in Q4.
**Action:** Implement quarterly inventory pre-staging protocols in August/September. Launch Q2 promotional campaigns (May–June) to smooth the demand curve.
**Estimated Impact:** Reducing Q4 logistics strain can cut overtime and expedite shipping costs by an estimated 10–15%, while Q2 promotions can incrementally lift the £425K–£475K monthly floor.

### R3: Return Rate Operational Programme
**Insight:** 16.47% of invoices are returns, yet return volume (5.3%) is low — indicating frequent, small-quantity returns consistent with defect or mislabelling issues.
**Action:** Flag top 20 returned SKUs for warehouse QA review before shipping. Cross-reference return invoices against product descriptions for accuracy.
**Estimated Impact:** A 20% reduction in the invoice return rate would recapture approximately £1.35M in annual gross revenue that currently flows back out as refunds.

### R4: VIP Retention Programme
**Insight:** HCV is extremely right-skewed. A small number of customers hold disproportionate value, while median spend is low.
**Action:** Segment customers into 3 tiers (HCV > £5,000 / £1,000–£5,000 / < £1,000). Offer the top tier exclusive early-access pricing on new product lines and dedicated account management.
**Estimated Impact:** Protecting even 10% of the revenue from the top HCV tier represents approximately £280K+ in protected recurring revenue.

---

## 12. Impact Estimation

| Recommendation | Mechanism | Estimated Impact |
|---|---|---|
| International AOV threshold | Minimum order to qualify for subsidised shipping | +£250K–£300K revenue annually |
| Q2 promotional calendar | Flash sales and email campaigns in May/June | +5–10% monthly revenue lift in off-peak months |
| Return rate reduction | SKU QA programme for top 20 returned items | Recapture of ~£1.35M currently processed as refunds |
| VIP retention programme | Tier-based loyalty and account management | Protection of £280K+ in high-HCV customer spend |

> Note: These estimates are based on directional inference from the data, not precision forecasting. They should be validated against actual cost-of-returns data and customer acquisition costs in a live business environment.

---

## 13. Limitations

1. **CustomerID Bias (~25% data exclusion):** Dropping 135,080 rows with missing CustomerID removes approximately a quarter of all revenue-generating transactions. All metrics in this report reflect registered customers only. Guest checkouts may behave differently and skew the population if included.

2. **Linear Regression Constraints:** The OLS demand model achieves an R-squared of 0.00, confirming that a linear model is inadequate for capturing the non-linear, heteroscedastic nature of retail transaction data. The model's value lies in directional coefficient significance, not predictive accuracy.

3. **Aggregation Limitations:** Country-level and product-level analyses are aggregated across the entire observation period. Time-varying effects (e.g., a spike in German orders in one quarter) are not captured in aggregate views.

4. **No Cost Data:** Without Cost of Goods Sold (COGS) data, true profitability analysis is impossible. Revenue and return rate are used as proxies for financial health.

5. **Observation Window:** The dataset covers only 13 months. Seasonal patterns cannot be confirmed as recurring without multi-year data.

---

## 14. Future Scope

1. **SKU-Level Non-Linear Price Elasticity Modelling:** Implement log-log regression or Bayesian models at the individual product level to compute actionable price elasticity coefficients per SKU.
2. **Predictive CLV Modelling:** Implement the BG/NBD + Gamma-Gamma framework to forecast future customer purchase probability and expected revenue — replacing the backward-looking HCV metric.
3. **Real-Time Dashboard:** Migrate the pipeline to a streaming architecture (e.g., Kafka + dbt + Tableau Hyper API) to provide live operational visibility rather than batch monthly reporting.
4. **Churn Prediction Model:** Train a classification model on recency, frequency, and monetary features to predict which high-HCV customers are at risk of churning.

---

## 15. Conclusion

This project delivered a production-grade end-to-end analytics pipeline on the UK Online Retail dataset. Starting from 541,909 raw transactional records, we implemented a deterministic ETL process, computed a rigorous KPI framework, validated hypotheses statistically, and assembled an interactive Tableau dashboard enabling dynamic business decision-making.

The core finding is clear: this business has strong structural revenue from a loyal registered customer base, but faces three urgent risks — extreme seasonal concentration, geographic market underdevelopment, and an unmanaged return rate. Acting on the four recommendations in this report — international threshold pricing, off-season promotions, a return SKU QA programme, and a VIP retention scheme — represents a realistic path to both protecting and growing revenue in the next fiscal year.

---

## 16. Appendix: Data Dictionary

| Field | Source | Type | Description |
|---|---|---|---|
| InvoiceNo | Raw | String | Unique invoice ID. 'C' prefix = return. |
| StockCode | Raw | String | Product code. |
| Description | Raw | String | Product name (cleaned/stripped). |
| Quantity | Raw | Integer | Units ordered. Negative = return. |
| InvoiceDate | Raw | Datetime | Transaction timestamp. |
| UnitPrice | Raw | Float | Price per unit in £. |
| CustomerID | Raw | String (post-clean) | Customer ID. NaN rows dropped. |
| Country | Raw | String | Country of customer. |
| Revenue | Engineered | Float | Quantity × UnitPrice. |
| IsReturn | Engineered | Boolean | True if InvoiceNo starts with 'C'. |
| IsDomestic | Engineered | Boolean | True if Country == 'United Kingdom'. |
| Year / Month / Hour | Engineered | Integer | Temporal features from InvoiceDate. |
| YearMonth | Engineered | String | Period aggregation for trend analysis. |
| Weekday | Engineered | String | Day name from InvoiceDate. |
| HCV | Computed | Float | Historical Customer Value (total spend per customer). |

---

## 17. Contribution Matrix

| Team Member | GitHub | Contribution Area |
|---|---|---|
| Shreyas Sarkar | @Shreyas-Sarkar | Repo setup, data ingestion pipeline, final integration & orchestration |
| Aditya Singh | @Mario5T | Data cleaning — missing value handling, return flagging, type standardization |
| Parth Singh | @parthz-13 | Feature engineering — Revenue, temporal features, HCV, KPI framework |
| Subhan Rai | @Subhan030 | Exploratory Data Analysis — trend analysis, country/product segmentation, EDA plots |
| Priyank Gaur | @Priyank-Gaur | Statistical analysis (regression, T-test, correlation), final report, Tableau assets |

---

*This report is submitted in partial fulfilment of the requirements for Capstone Project 2 at Newton School of Technology.*
*All analysis is derived strictly from the UCI Online Retail Dataset. No external data or pre-cleaned datasets were used.*
