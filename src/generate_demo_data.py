from pathlib import Path

import numpy as np
import pandas as pd


np.random.seed(42)
out = Path("data/raw")
out.mkdir(parents=True, exist_ok=True)

education = ["Graduation", "PhD", "Master", "2n Cycle", "Basic"]
marital = ["Married", "Together", "Single", "Divorced", "Widow"]

rows = []
for i in range(1, 2201):
    income = int(np.clip(np.random.normal(52000, 21000), 8000, 170000))
    kidhome = int(np.random.choice([0, 1, 2], p=[0.58, 0.34, 0.08]))
    teenhome = int(np.random.choice([0, 1, 2], p=[0.62, 0.32, 0.06]))
    recency = int(np.random.randint(0, 100))
    value_base = income / 120 + np.random.gamma(2.2, 90) - kidhome * 35 - teenhome * 25
    mnt_wines = int(max(0, np.random.normal(value_base * 0.42, 70)))
    mnt_meat = int(max(0, np.random.normal(value_base * 0.30, 65)))
    mnt_gold = int(max(0, np.random.normal(value_base * 0.14, 35)))
    mnt_fish = int(max(0, np.random.normal(value_base * 0.08, 25)))
    mnt_fruits = int(max(0, np.random.normal(value_base * 0.04, 20)))
    mnt_sweets = int(max(0, np.random.normal(value_base * 0.03, 18)))
    web_visits = int(np.random.poisson(5))
    web_purchases = int(max(0, np.random.poisson(3 + income / 50000 - recency / 100)))
    store_purchases = int(max(0, np.random.poisson(4 + income / 45000)))
    catalog_purchases = int(max(0, np.random.poisson(2 + income / 70000)))
    response_probability = 1 / (1 + np.exp(-(-2.2 + income / 80000 + (recency < 25) * 0.8 + (web_purchases > 4) * 0.5)))
    response = int(np.random.random() < response_probability)
    rows.append(
        {
            "ID": i,
            "Year_Birth": int(np.random.randint(1945, 1998)),
            "Education": str(np.random.choice(education, p=[0.48, 0.16, 0.18, 0.12, 0.06])),
            "Marital_Status": str(np.random.choice(marital, p=[0.38, 0.26, 0.22, 0.10, 0.04])),
            "Income": income,
            "Kidhome": kidhome,
            "Teenhome": teenhome,
            "Dt_Customer": "2014-01-01",
            "Recency": recency,
            "MntWines": mnt_wines,
            "MntFruits": mnt_fruits,
            "MntMeatProducts": mnt_meat,
            "MntFishProducts": mnt_fish,
            "MntSweetProducts": mnt_sweets,
            "MntGoldProds": mnt_gold,
            "NumDealsPurchases": int(np.random.poisson(2)),
            "NumWebPurchases": web_purchases,
            "NumCatalogPurchases": catalog_purchases,
            "NumStorePurchases": store_purchases,
            "NumWebVisitsMonth": web_visits,
            "AcceptedCmp1": int(np.random.random() < response_probability * 0.45),
            "AcceptedCmp2": int(np.random.random() < response_probability * 0.30),
            "AcceptedCmp3": int(np.random.random() < response_probability * 0.35),
            "AcceptedCmp4": int(np.random.random() < response_probability * 0.25),
            "AcceptedCmp5": int(np.random.random() < response_probability * 0.20),
            "Response": response,
        }
    )

pd.DataFrame(rows).to_csv(out / "marketing_campaign.csv", index=False)
print("Created data/raw/marketing_campaign.csv")

