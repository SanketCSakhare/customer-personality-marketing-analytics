# Kaggle Download Instructions

Dataset: [Customer Personality Analysis](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)

## Manual Download

1. Open the Kaggle dataset page.
2. Click **Download**.
3. Extract the ZIP file.
4. Copy `marketing_campaign.csv` into:

```text
data/raw/marketing_campaign.csv
```

## Kaggle API Option

If the Kaggle API is configured on your machine:

```powershell
kaggle datasets download -d imakash3011/customer-personality-analysis -p data/raw --unzip
```

The analysis script expects:

```text
data/raw/marketing_campaign.csv
```

If the Kaggle download is not available, run the demo generator:

```powershell
python src/generate_demo_data.py
```

