# Data Sources

## Primary Source

This project uses public data from the U.S. Department of the Treasury Daily Treasury Statement.

The source data was downloaded as CSV files and imported into Power BI using Power Query.

## Source Tables

| # | Source Table | File | Coverage |
|---|---|---|---|
| 1 | Operating Cash Balance | DTS_OpCashBal_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 2 | Deposits and Withdrawals of Operating Cash | DTS_OpCashDpstWdrl_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 3 | Public Debt Transactions | DTS_PubDebtTrans_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 4 | Adjustment of Public Debt Transactions to Cash Basis | DTS_PubDebtCashAdj_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 5 | Debt Subject to Limit | DTS_DebtSubjLim_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 6 | Income Tax Refunds Issued | DTS_IncmTaxRfnd_20160101_20260924.csv | 01/04/2016 - 09/24/2026 |
| 7 | Federal Tax Deposits | DTS_FedTaxDpst_20160101_20260924.csv | 01/04/2016 - 02/13/2023 |
| 8 | Interagency Tax Transfers | DTS_InterAgencyTaxTransfers_20160101_20260924.csv | 02/14/2023 - 09/24/2026 |
| 9 | Short-Term Cash Investments | DTS_StCashInvest_20160101_20260924.csv | 01/04/2016 - 02/13/2023 |

## Coverage Notes

The source tables do not all cover identical reporting periods.

In particular:

- Federal Tax Deposits ends on 02/13/2023.
- Short-Term Cash Investments ends on 02/13/2023.
- Interagency Tax Transfers begins on 02/14/2023.
- Most other source tables continue through 09/24/2026.

These differences are documented in the Power BI report and were considered when creating comparisons and summary measures.

## Power Query Import

The final report uses CSV versions of the Treasury data rather than the original Excel extracts used during early development.

Each CSV is imported directly with Power Query, headers are promoted, and column data types are explicitly assigned.

Additional modeling fields were created where needed, including:

- Refund cash direction
- Investment flow direction
- Tax row classification
- Debt and reconciliation helper measures

## Refresh Considerations

The PBIX file currently references local source paths used during development.

A user downloading the project may need to update the Power Query file paths before refreshing the model on another computer.

The included PDF and screenshots can be reviewed without refreshing the source data.
