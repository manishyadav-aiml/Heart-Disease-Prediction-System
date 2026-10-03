"""
Creates a SYNTHETIC demo file dataset/heart.csv (303 rows, same columns as the
real heart disease dataset) so that the project runs out of the box.

The values are random and only loosely follow medical patterns. Predictions made
with a model trained on this file are NOT meaningful.

To use real data: replace dataset/heart.csv with the real file, delete
dataset/DEMO_DATA.txt and run:  python train_model.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(42)
n = 303

age = rng.integers(29, 78, n)
sex = rng.choice([0, 1], n, p=[0.32, 0.68])
cp = rng.choice([0, 1, 2, 3], n, p=[0.47, 0.17, 0.29, 0.07])
trestbps = np.clip(rng.normal(131, 17, n), 94, 200).astype(int)
chol = np.clip(rng.normal(246, 52, n), 126, 564).astype(int)
fbs = rng.choice([0, 1], n, p=[0.85, 0.15])
restecg = rng.choice([0, 1, 2], n, p=[0.50, 0.49, 0.01])
thalach = np.clip(rng.normal(150, 23, n) - (age - 54) * 0.6, 71, 202).astype(int)
exang = rng.choice([0, 1], n, p=[0.67, 0.33])
oldpeak = np.round(np.clip(rng.gamma(1.2, 0.9, n), 0, 6.2), 1)
slope = rng.choice([0, 1, 2], n, p=[0.07, 0.46, 0.47])
ca = rng.choice([0, 1, 2, 3, 4], n, p=[0.58, 0.22, 0.13, 0.06, 0.01])
thal = rng.choice([0, 1, 2, 3], n, p=[0.01, 0.06, 0.55, 0.38])

score = (
    0.04 * (age - 54) + 0.8 * sex + 0.5 * (cp == 0) - 0.8 * (cp >= 1)
    + 0.012 * (trestbps - 131) + 0.003 * (chol - 246)
    - 0.03 * (thalach - 150) + 1.0 * exang + 0.6 * oldpeak
    + 0.9 * ca + 0.7 * (thal == 3) - 1.5
)
prob = 1 / (1 + np.exp(-(score + rng.normal(0, 0.9, n))))
target = (rng.random(n) < prob).astype(int)

df = pd.DataFrame({
    "age": age, "sex": sex, "cp": cp, "trestbps": trestbps, "chol": chol,
    "fbs": fbs, "restecg": restecg, "thalach": thalach, "exang": exang,
    "oldpeak": oldpeak, "slope": slope, "ca": ca, "thal": thal, "target": target,
})
df.to_csv(HERE / "heart.csv", index=False)
(HERE / "DEMO_DATA.txt").write_text(
    "heart.csv in this folder is SYNTHETIC demo data.\n"
    "Replace it with the real heart disease dataset, delete this file,\n"
    "then run: python train_model.py\n",
    encoding="utf-8",
)
print(f"Demo dataset written: {len(df)} rows, {int(df.target.sum())} positive")
