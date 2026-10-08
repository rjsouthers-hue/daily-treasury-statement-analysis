# Methodology

## Project Scope

This project analyzes U.S. Daily Treasury Statement data in Power BI with a focus on Treasury General Account cash activity, public debt financing, tax-related cash flows, federal debt composition, and reconciliation controls.

The report primarily covers January 2016 through September 2026, although some Treasury source tables have shorter reporting periods.

## Cash Flow Conventions

For analytical consistency, cash movements are modeled using the following sign conventions:

- TGA deposits are treated as positive cash flow.
- TGA withdrawals are treated as negative cash flow.
- Income tax refunds are converted to negative cash effect for trend analysis.
- Short-term cash investment deposits are treated as positive and withdrawals as negative.

These conventions allow inflows and outflows from separate Treasury tables to be compared on a common cash-flow basis.

## TGA Reconciliation

Treasury General Account activity is reconciled using:

Opening Balance  
+ Deposits  
- Withdrawals  
= Calculated Closing Balance

The calculated closing balance is then compared with the published closing balance.

A difference of zero indicates a full reconciliation for the selected record date.

## Debt Financing Reconciliation

Gross public debt transactions are not assumed to equal TGA cash activity directly.

The report therefore follows this sequence:

Gross Public Debt Transactions  
→ Cash-Basis Adjustments  
→ TGA Deposits and Withdrawals

Adjusted debt issuance cash is compared with corresponding TGA debt-issue deposits.

Adjusted debt redemption cash is compared with corresponding TGA debt-redemption withdrawals.

Small differences may remain because source values are reported in USD millions and transaction-level detail may differ slightly from published totals.

## Debt Position and Statutory Limit

Total federal debt is calculated as:

Debt Held by the Public  
+ Intragovernmental Holdings

Debt Subject to Limit is calculated by adjusting total federal debt for:

- Debt Not Subject to Limit
- Other Debt Subject to Limit

Statutory debt-limit values reported as zero are treated as unavailable for historical trend purposes rather than interpreted as a literal zero-dollar debt limit.

## Date Handling

Most report pages allow a selected date range for historical analysis.

Measures used for headline balances generally evaluate the latest date in the selected period.

The Debt Financing and TGA Cash page uses a single selected record date because its reconciliation logic compares daily debt activity with daily TGA activity.

If no debt-page date is explicitly selected, the report defaults to the latest common date available across the required debt and TGA source tables.

## Data Coverage

Treasury source tables do not all cover identical time periods.

In particular:

- Federal Tax Deposits ends on 02/13/2023.
- Short-Term Cash Investments ends on 02/13/2023.
- Interagency Tax Transfers begins on 02/14/2023.

Measures and report notes are designed to avoid presenting incompatible reporting periods as directly comparable where possible.

## Validation

The final report includes a dedicated Reconciliation and Data Notes page containing checks for:

- TGA cash-flow reconciliation
- Debt issuance cash tie-out
- Debt redemption cash tie-out
- Debt position calculation

Status indicators distinguish balanced results, minor variances, larger differences, and unavailable comparisons.
