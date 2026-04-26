# Data Dictionary

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
| HCV | Computed | Float | Historical Customer Value (total spend). |
