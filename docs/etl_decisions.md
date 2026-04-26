# Cleaning Decisions Log

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
These are removed as they carry no commercial meaning.
