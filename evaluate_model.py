from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
DATA = pd.read_csv(BASE / "dataset.csv")
location_encoder = joblib.load(BASE / "location_encoder.pkl")
area_encoder = joblib.load(BASE / "area_encoder.pkl")
property_encoder = joblib.load(BASE / "property_encoder.pkl")

cols = ["location", "area_in_sqft", "rate_per_sqft", "area_type", "property_type", "bhk_type", "price_in_cr"]
df = DATA[cols].copy()
df = df.dropna(subset=["price_in_cr", "area_in_sqft", "rate_per_sqft", "area_type", "property_type", "bhk_type"])
df = df[(df["price_in_cr"] > 0) & (df["price_in_cr"] < 10) & (df["area_in_sqft"] > 0) & (df["rate_per_sqft"] >= 0)]
df["location"] = df["location"].fillna("Unknown").astype(str)

# Reuse the saved encoders so categories map consistently with the deployed model.
df = df[df["location"].isin(location_encoder.classes_)]
df = df[df["area_type"].isin(area_encoder.classes_) & df["property_type"].isin(property_encoder.classes_)]
df["location"] = location_encoder.transform(df["location"])
df["area_type"] = area_encoder.transform(df["area_type"])
df["property_type"] = property_encoder.transform(df["property_type"])
feature_cols = ["location", "area_in_sqft", "rate_per_sqft", "area_type", "property_type", "bhk_type"]
X, y = df[feature_cols], df["price_in_cr"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=150, max_depth=20, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)
pred = model.predict(X_test)
rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
print(f"Rows evaluated: {len(df):,}")
print(f"Train rows: {len(X_train):,} | Test rows: {len(X_test):,}")
print(f"R²:   {r2_score(y_test, pred):.4f}")
print(f"MAE:  {mean_absolute_error(y_test, pred):.4f} crore")
print(f"RMSE: {rmse:.4f} crore")
print("Note: this is a fresh hold-out evaluation, not a guarantee of future-market accuracy.")
