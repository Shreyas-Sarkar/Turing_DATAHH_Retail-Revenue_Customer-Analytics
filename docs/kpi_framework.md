# KPI Framework

| KPI | Formula | Business Purpose |
|---|---|---|
| Total Revenue | SUM(Revenue) where not IsReturn | Core monetary health |
| AOV | MEAN(Revenue per InvoiceNo) | Cart size efficiency |
| Return Rate (Invoice) | Returned Invoices / Total Invoices | Operational drag |
| Return Rate (Volume) | ABS(Neg Qty) / Pos Qty | Product defect proxy |
| HCV | Total spend per CustomerID (historical) | Customer value segmentation |
| Purchase Frequency | Distinct InvoiceNo per CustomerID | Loyalty proxy |

> Note: HCV = Historical Customer Value. This is NOT a predictive CLV model.
> It reflects cumulative spend within the observation window only.
