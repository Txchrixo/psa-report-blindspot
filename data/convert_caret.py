"""Convert the CARET PSA data (R package AROC, file psa.rda) to a CSV file.

Run from the root of the repository:
    pip install pyreadr pandas
    python data/convert_caret.py
"""

from pathlib import Path

import pyreadr

RAW_DIR = Path("data/raw")
SOURCE = RAW_DIR / "psa.rda"
TARGET = RAW_DIR / "caret_psa_serial.csv"

df = pyreadr.read_r(str(SOURCE))["psa"]

df = df.rename(columns={
    "marker1": "psa_total_ng_ml",          # total PSA, ng/mL
    "marker2": "free_to_total_ratio",      # free PSA / total PSA (0.20 = 20%)
    "status": "cancer_case",               # 1 = later diagnosed with prostate cancer, 0 = control
    "t": "years_from_diagnosis",           # time of the blood draw relative to diagnosis
})
df["id"] = df["id"].astype(int)
df["cancer_case"] = df["cancer_case"].astype(int)

df.to_csv(TARGET, index=False)

men = df.groupby("id")
print(f"Saved {TARGET}")
print(f"Rows (blood draws): {len(df)}")
print(f"Men: {df['id'].nunique()}")
print(f"Cancer cases: {df.loc[df.cancer_case == 1, 'id'].nunique()}, "
      f"controls: {df.loc[df.cancer_case == 0, 'id'].nunique()}")
print(f"Draws per man: from {men.size().min()} to {men.size().max()}")
print()
print(df.head(10).to_string(index=False))