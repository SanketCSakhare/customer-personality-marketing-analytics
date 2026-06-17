from pathlib import Path

import pandas as pd


RAW_PATH = Path("data/raw/marketing_campaign.csv")
PROCESSED_DIR = Path("data/processed")
CHART_DIR = Path("dashboard/screenshots")


def read_marketing_data(path):
    try:
        df = pd.read_csv(path, sep="\t")
        if len(df.columns) > 1:
            return df
    except Exception:
        pass
    return pd.read_csv(path)


def income_band(income):
    if income < 30000:
        return "01. <30k"
    if income < 50000:
        return "02. 30k-50k"
    if income < 75000:
        return "03. 50k-75k"
    if income < 100000:
        return "04. 75k-100k"
    return "05. 100k+"


def segment(row):
    if row["customer_value"] >= 900 and row["Response"] == 1:
        return "High-value responders"
    if row["customer_value"] >= 900 and row["Recency"] >= 55:
        return "High-value at-risk"
    if row["NumWebVisitsMonth"] >= 6 and row["NumWebPurchases"] <= 2:
        return "Digital browsers"
    if row["customer_value"] >= 500:
        return "Growth customers"
    return "Low-value nurture"


def targeting_action(row):
    if row["customer_segment"] == "High-value responders":
        return "Premium loyalty and cross-sell"
    if row["customer_segment"] == "High-value at-risk":
        return "Win-back offer"
    if row["customer_segment"] == "Digital browsers":
        return "Digital conversion campaign"
    if row["customer_segment"] == "Growth customers":
        return "Product bundle recommendation"
    return "Monitor"


def svg_bar_chart(df, label_col, value_col, title, output_path, value_format="{:.1%}"):
    width = 960
    height = 500
    margin_left = 250
    margin_right = 90
    margin_top = 72
    bar_gap = 18
    bar_height = 42
    plot_width = width - margin_left - margin_right
    max_value = max(df[value_col].max(), 0.01)
    rows = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="32" y="42" font-family="Arial" font-size="24" font-weight="700" fill="#172033">{title}</text>',
    ]
    for idx, row in df.reset_index(drop=True).iterrows():
        y = margin_top + idx * (bar_height + bar_gap)
        bar_width = int((row[value_col] / max_value) * plot_width)
        rows.extend(
            [
                f'<text x="32" y="{y + 28}" font-family="Arial" font-size="15" fill="#172033">{row[label_col]}</text>',
                f'<rect x="{margin_left}" y="{y}" width="{bar_width}" height="{bar_height}" rx="4" fill="#be185d"/>',
                f'<text x="{margin_left + bar_width + 12}" y="{y + 28}" font-family="Arial" font-size="15" fill="#172033">{value_format.format(row[value_col])}</text>',
            ]
        )
    rows.append("</svg>")
    output_path.write_text("\n".join(rows), encoding="utf-8")


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = read_marketing_data(RAW_PATH)
    df = df.dropna(subset=["Income"]).copy()
    spend_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
    campaign_cols = [col for col in ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"] if col in df.columns]
    df["customer_value"] = df[spend_cols].sum(axis=1)
    df["total_purchases"] = df[["NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]].sum(axis=1)
    df["web_purchase_share"] = df["NumWebPurchases"] / df["total_purchases"].clip(lower=1)
    df["store_purchase_share"] = df["NumStorePurchases"] / df["total_purchases"].clip(lower=1)
    df["campaign_acceptances"] = df[campaign_cols].sum(axis=1)
    df["income_band"] = df["Income"].apply(income_band)
    df["has_children"] = ((df["Kidhome"] + df["Teenhome"]) > 0).astype(int)
    df["customer_segment"] = df.apply(segment, axis=1)
    df["targeting_action"] = df.apply(targeting_action, axis=1)

    segment_summary = (
        df.groupby("customer_segment", as_index=False)
        .agg(
            customers=("ID", "count"),
            response_rate=("Response", "mean"),
            avg_customer_value=("customer_value", "mean"),
            total_customer_value=("customer_value", "sum"),
            avg_recency=("Recency", "mean"),
            web_purchase_share=("web_purchase_share", "mean"),
        )
        .sort_values("avg_customer_value", ascending=False)
    )
    response_summary = (
        df.groupby("income_band", as_index=False)
        .agg(
            customers=("ID", "count"),
            response_rate=("Response", "mean"),
            avg_customer_value=("customer_value", "mean"),
            avg_recency=("Recency", "mean"),
        )
        .sort_values("income_band")
    )
    product_summary = pd.DataFrame(
        {
            "product_category": ["Wine", "Fruits", "Meat", "Fish", "Sweets", "Gold"],
            "total_spend": [df[col].sum() for col in spend_cols],
            "avg_spend": [df[col].mean() for col in spend_cols],
        }
    ).sort_values("total_spend", ascending=False)
    targeting_summary = (
        df.groupby("targeting_action", as_index=False)
        .agg(
            customers=("ID", "count"),
            response_rate=("Response", "mean"),
            avg_customer_value=("customer_value", "mean"),
            total_customer_value=("customer_value", "sum"),
        )
        .sort_values("avg_customer_value", ascending=False)
    )
    targeting_queue = df[df["targeting_action"] != "Monitor"].sort_values(["customer_value", "Response"], ascending=[False, False]).head(300)

    df.to_csv(PROCESSED_DIR / "customers_marketing_scored.csv", index=False)
    segment_summary.to_csv(PROCESSED_DIR / "segment_summary.csv", index=False)
    response_summary.to_csv(PROCESSED_DIR / "campaign_response_summary.csv", index=False)
    product_summary.to_csv(PROCESSED_DIR / "product_category_summary.csv", index=False)
    targeting_summary.to_csv(PROCESSED_DIR / "targeting_recommendations.csv", index=False)
    targeting_queue.to_csv(PROCESSED_DIR / "priority_targeting_queue.csv", index=False)

    svg_bar_chart(
        segment_summary,
        "customer_segment",
        "response_rate",
        "Campaign Response Rate by Segment",
        CHART_DIR / "response_rate_by_segment.svg",
    )
    svg_bar_chart(
        segment_summary,
        "customer_segment",
        "avg_customer_value",
        "Average Customer Value by Segment",
        CHART_DIR / "customer_value_by_segment.svg",
        value_format="{:.0f}",
    )
    print("Created marketing segmentation outputs, targeting queue, and SVG charts.")


if __name__ == "__main__":
    main()
