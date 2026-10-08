from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).resolve().parent
CHARTS_DIR = SCRIPT_DIR / "charts"
CHARTS_DIR.mkdir(exist_ok=True)


# ============================================================
# 1. LOAD DATA
# ============================================================

data = pd.read_csv(
    r"C:\Users\rsout\OneDrive\Job Search\Portfolio\Treasury Financial Intelligence\Data\Daily Treasury CSVs (01.01.2016-Current)\DTS_IncmTaxRfnd_20160101_20260924.csv"
)


# ============================================================
# 2. PREPARE DATA
# ============================================================

data["Record Date"] = pd.to_datetime(data["Record Date"])
data["Year Month"] = data["Record Date"].dt.to_period("M")


# ============================================================
# 3. DATASET OVERVIEW
# ============================================================

start_date = data["Record Date"].min()
end_date = data["Record Date"].max()
record_count = len(data)

print("\n" + "=" * 60)
print("TREASURY TAX REFUND ANALYSIS")
print("=" * 60)

print(f"Records analyzed: {record_count:,}")
print(f"Date range: {start_date:%Y-%m-%d} to {end_date:%Y-%m-%d}")


# ============================================================
# 4. REFUND ACTIVITY BY TYPE
# ============================================================

refund_summary = (
    data.groupby("Federal Tax Refund Type")["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
    .sort_values("Federal Tax Refunds Today", ascending=False)
)

total_refunds = refund_summary["Federal Tax Refunds Today"].sum()

refund_summary["Percent of Total"] = (
    refund_summary["Federal Tax Refunds Today"]
    / total_refunds
    * 100
).round(2)


# ============================================================
# 5. REFUND ACTIVITY BY MONTH
# ============================================================

monthly_summary = (
    data.groupby("Year Month")
    .agg(
        Total_Refund_Activity=(
            "Federal Tax Refunds Today",
            "sum"
        ),
        Average_Daily_Activity=(
            "Federal Tax Refunds Today",
            "mean"
        )
    )
    .reset_index()
)

monthly_summary["Average_Daily_Activity"] = (
    monthly_summary["Average_Daily_Activity"].round(2)
)

top_months = (
    monthly_summary
    .sort_values("Total_Refund_Activity", ascending=False)
    .head(10)
)

average_monthly_activity = (
    monthly_summary["Total_Refund_Activity"].mean()
)

monthly_summary["Percent of Average"] = (
    monthly_summary["Total_Refund_Activity"]
    / average_monthly_activity
    * 100
).round(2)

high_activity_months = monthly_summary[
    monthly_summary["Percent of Average"] >= 200
]


# ============================================================
# 6. HIGH-ACTIVITY MONTH ANALYSIS
# ============================================================

high_activity_data = data[
    data["Year Month"].isin(
        high_activity_months["Year Month"]
    )
]

high_activity_by_type = (
    high_activity_data
    .groupby("Federal Tax Refund Type")["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
    .sort_values("Federal Tax Refunds Today", ascending=False)
)


# ============================================================
# 7. MARCH 2021 INVESTIGATION
# ============================================================

march_2021 = data[
    data["Year Month"] == pd.Period("2021-03")
]

march_2021_by_type = (
    march_2021
    .groupby("Federal Tax Refund Type")["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
    .sort_values("Federal Tax Refunds Today", ascending=False)
)

march_2021_total = (
    march_2021_by_type["Federal Tax Refunds Today"].sum()
)

march_2021_by_type["Percent of Month"] = (
    march_2021_by_type["Federal Tax Refunds Today"]
    / march_2021_total
    * 100
).round(2)


# ============================================================
# 8. ECONOMIC IMPACT PAYMENT ANALYSIS
# ============================================================

eip_data = data[
    data["Federal Tax Refund Type"].str.contains(
        "Economic Impact Payments"
    )
]

eip_monthly = (
    eip_data
    .groupby("Year Month")["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
    .sort_values("Federal Tax Refunds Today", ascending=False)
)

total_eip_activity = (
    eip_monthly["Federal Tax Refunds Today"].sum()
)

march_2021_eip = eip_monthly.loc[
    eip_monthly["Year Month"] == pd.Period("2021-03"),
    "Federal Tax Refunds Today"
].iloc[0]

march_2021_eip_percent = (
    march_2021_eip
    / total_eip_activity
    * 100
)


# ============================================================
# 9. ECONOMIC IMPACT PAYMENTS BY PAYMENT METHOD
# ============================================================

eip_by_method = (
    eip_data
    .groupby(
        ["Year Month", "Federal Tax Refund Type"]
    )["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
)

eip_by_method_active = eip_by_method[
    eip_by_method["Federal Tax Refunds Today"] != 0
]

eip_chart_data = (
    eip_by_method_active[
        eip_by_method_active["Federal Tax Refunds Today"] > 0
    ]
    .pivot(
        index="Year Month",
        columns="Federal Tax Refund Type",
        values="Federal Tax Refunds Today"
    )
    .fillna(0)
)


# ============================================================
# 10. SEASONAL REFUND ACTIVITY
# ============================================================

monthly_summary["Calendar Month"] = (
    monthly_summary["Year Month"].dt.month
)

seasonal_summary = (
    monthly_summary
    .groupby("Calendar Month")["Total_Refund_Activity"]
    .mean()
    .reset_index()
)

seasonal_summary["Month Name"] = (
    seasonal_summary["Calendar Month"]
    .apply(
        lambda x: pd.Timestamp(2020, x, 1).strftime("%B")
    )
)

seasonal_summary["Average Monthly Activity"] = (
    seasonal_summary["Total_Refund_Activity"].round(2)
)


# ============================================================
# 11. SEASONAL ACTIVITY EXCLUDING SPECIAL PAYMENTS
# ============================================================

regular_refunds = data[
    ~data["Federal Tax Refund Type"].str.contains(
        "Economic Impact Payments|Advanced Child Tax Credit",
        regex=True
    )
]

regular_monthly_summary = (
    regular_refunds
    .groupby("Year Month")["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
)

regular_monthly_summary["Calendar Month"] = (
    regular_monthly_summary["Year Month"].dt.month
)

regular_seasonal_summary = (
    regular_monthly_summary
    .groupby("Calendar Month")["Federal Tax Refunds Today"]
    .mean()
    .reset_index()
)

regular_seasonal_summary["Month Name"] = (
    regular_seasonal_summary["Calendar Month"]
    .apply(
        lambda x: pd.Timestamp(2020, x, 1).strftime("%B")
    )
)

regular_seasonal_summary["Average Monthly Activity"] = (
    regular_seasonal_summary["Federal Tax Refunds Today"].round(2)
)


# ============================================================
# 12. SEASONAL ACTIVITY BY REFUND TYPE
# ============================================================

regular_refund_type_monthly = (
    regular_refunds
    .groupby(
        ["Year Month", "Federal Tax Refund Type"]
    )["Federal Tax Refunds Today"]
    .sum()
    .reset_index()
)

regular_refund_type_monthly["Calendar Month"] = (
    regular_refund_type_monthly["Year Month"].dt.month
)

seasonal_by_type = (
    regular_refund_type_monthly
    .groupby(
        ["Calendar Month", "Federal Tax Refund Type"]
    )["Federal Tax Refunds Today"]
    .mean()
    .reset_index()
)

seasonal_by_type["Month Name"] = (
    seasonal_by_type["Calendar Month"]
    .apply(
        lambda x: pd.Timestamp(2020, x, 1).strftime("%B")
    )
)

seasonal_by_type["Average Monthly Activity"] = (
    seasonal_by_type["Federal Tax Refunds Today"].round(2)
)


# ============================================================
# 13. TOP REFUND TYPE BY CALENDAR MONTH
# ============================================================

top_seasonal_types = seasonal_by_type.loc[
    seasonal_by_type.groupby("Calendar Month")[
        "Average Monthly Activity"
    ].idxmax()
].copy()


# ============================================================
# 14. TOP REFUND TYPE SHARE BY CALENDAR MONTH
# ============================================================

monthly_totals = regular_seasonal_summary[
    [
        "Calendar Month",
        "Average Monthly Activity"
    ]
].copy()

monthly_totals = monthly_totals.rename(
    columns={
        "Average Monthly Activity":
        "Total Average Monthly Activity"
    }
)

top_monthly_types = seasonal_by_type.loc[
    seasonal_by_type.groupby("Calendar Month")[
        "Average Monthly Activity"
    ].idxmax()
].copy()

top_monthly_types = top_monthly_types.merge(
    monthly_totals,
    on="Calendar Month"
)

top_monthly_types["Percent of Monthly Activity"] = (
    top_monthly_types["Average Monthly Activity"]
    / top_monthly_types["Total Average Monthly Activity"]
    * 100
).round(2)


# ============================================================
# 15. SUMMARY OF KEY FINDINGS
# ============================================================

highest_activity_month = (
    monthly_summary
    .sort_values("Total_Refund_Activity", ascending=False)
    .iloc[0]
)

peak_seasonal_month = (
    regular_seasonal_summary
    .sort_values("Average Monthly Activity", ascending=False)
    .iloc[0]
)

print("\n" + "-" * 60)
print("KEY FINDINGS")
print("-" * 60)

print(
    f"Average monthly refund activity: "
    f"{average_monthly_activity:,.0f}"
)

print(
    f"Highest activity month: "
    f"{highest_activity_month['Year Month']} "
    f"({highest_activity_month['Total_Refund_Activity']:,.0f})"
)

print(
    f"March 2021 EIP share: "
    f"{march_2021_eip_percent:.2f}%"
)

print(
    f"Peak regular refund month: "
    f"{peak_seasonal_month['Month Name']} "
    f"({peak_seasonal_month['Average Monthly Activity']:,.0f} average)"
)

print(
    "\nAnalysis complete. "
    "Charts will open as they are generated."
)


# ============================================================
# 16. MONTHLY REFUND ACTIVITY VISUALIZATION
# ============================================================

plt.figure(figsize=(14, 7))

months = monthly_summary["Year Month"].astype(str)
activity = monthly_summary["Total_Refund_Activity"]

plt.plot(months, activity)

plt.title("Monthly Treasury Tax Refund Activity")
plt.xlabel("Month")
plt.ylabel("Refund Activity")

plt.xticks(
    range(0, len(monthly_summary), 12),
    months[::12],
    rotation=45
)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x:,.0f}")
)

march_2021_index = monthly_summary.index[
    monthly_summary["Year Month"] == pd.Period("2021-03")
][0]

march_2021_activity = monthly_summary.loc[
    march_2021_index,
    "Total_Refund_Activity"
]

plt.scatter(
    march_2021_index,
    march_2021_activity
)

plt.annotate(
    "March 2021\n446,855",
    (
        march_2021_index,
        march_2021_activity
    ),
    xytext=(35, -45),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->")
)

plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "monthly_refund_activity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# 17. ECONOMIC IMPACT PAYMENT VISUALIZATION
# ============================================================

eip_monthly_chronological = (
    eip_monthly
    .sort_values("Year Month")
)

plt.figure(figsize=(14, 7))

eip_months = eip_monthly_chronological[
    "Year Month"
].astype(str)

eip_activity = eip_monthly_chronological[
    "Federal Tax Refunds Today"
]

plt.plot(
    eip_months,
    eip_activity
)

plt.title("Monthly Economic Impact Payment Activity")
plt.xlabel("Month")
plt.ylabel("Refund Activity")

plt.xticks(
    rotation=45
)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "economic_impact_payments.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 18. ECONOMIC IMPACT PAYMENTS BY PAYMENT METHOD
# ============================================================

eip_chart_data.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 7)
)

plt.title("Economic Impact Payment Activity by Payment Method")
plt.xlabel("Month")
plt.ylabel("Refund Activity")

plt.xticks(rotation=45)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "eip_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 19. SEASONAL REFUND ACTIVITY VISUALIZATION
# ============================================================

plt.figure(figsize=(12, 7))

plt.bar(
    regular_seasonal_summary["Month Name"],
    regular_seasonal_summary["Average Monthly Activity"]
)

plt.title("Average Monthly Refund Activity by Calendar Month")
plt.xlabel("Month")
plt.ylabel("Average Refund Activity")

plt.xticks(rotation=45)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "seasonal_refund_activity.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 20. SEASONAL REFUND ACTIVITY BY TYPE VISUALIZATION
# ============================================================

seasonal_chart_data = seasonal_by_type.pivot(
    index="Month Name",
    columns="Federal Tax Refund Type",
    values="Average Monthly Activity"
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

seasonal_chart_data = seasonal_chart_data.reindex(
    month_order
)

seasonal_chart_data.plot(
    kind="line",
    figsize=(14, 7)
)

plt.title("Average Monthly Refund Activity by Refund Type")
plt.xlabel("Month")
plt.ylabel("Average Refund Activity")

plt.xticks(rotation=45)

plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f"{x:,.0f}")
)

plt.legend(
    title="Refund Type",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    CHARTS_DIR / "seasonal_refund_by_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 21. FINAL SEASONAL SUMMARY
# ============================================================

print("\n" + "-" * 60)
print("TOP REFUND TYPE BY CALENDAR MONTH")
print("-" * 60)

print(
    top_seasonal_types[
        [
            "Month Name",
            "Federal Tax Refund Type",
            "Average Monthly Activity"
        ]
    ].to_string(index=False)
)

print("\n" + "-" * 60)
print("TOP REFUND TYPE SHARE BY CALENDAR MONTH")
print("-" * 60)

print(
    top_monthly_types[
        [
            "Month Name",
            "Federal Tax Refund Type",
            "Average Monthly Activity",
            "Percent of Monthly Activity"
        ]
    ].to_string(index=False)
)

print("\n" + "=" * 60)
print("TREASURY TAX REFUND ANALYSIS COMPLETE")
print("=" * 60)