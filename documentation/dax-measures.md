# Selected DAX Measures

This file highlights a representative set of DAX measures used in the report.

The full Power BI model contains additional helper and page-specific measures.

## TGA Reconciliation

### Calculated Closing Balance

```DAX
TGA Calculated Closing (USD millions) =
[TGA Opening (USD millions)]
+ [TGA Deposits (USD millions)]
- [TGA Withdrawals (USD millions)]
