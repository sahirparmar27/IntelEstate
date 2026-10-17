"""Intel Estate: Ahmedabad property valuation prototype."""
from pathlib import Path
import difflib
import logging
import re

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
logging.basicConfig(level=logging.INFO)

# Load artifacts relative to this file, not the shell's current directory.
model = joblib.load(BASE_DIR / "model.pkl")
location_encoder = joblib.load(BASE_DIR / "location_encoder.pkl")
area_encoder = joblib.load(BASE_DIR / "area_encoder.pkl")
property_encoder = joblib.load(BASE_DIR / "property_encoder.pkl")

locations = [str(x) for x in location_encoder.classes_]
area_types = [str(x) for x in area_encoder.classes_ if str(x).lower() != "plot"]
property_types = [str(x) for x in property_encoder.classes_ if str(x).lower() not in {"floor", "land"}]

# The model was trained with rate_per_sqft as a feature. Use the dataset's
# median rate for the matched location where available, rather than a fixed
# value. The global median is a documented fallback for sparse locations.
dataset_path = BASE_DIR / "dataset.csv"
try:
    _df = pd.read_csv(dataset_path, usecols=["location", "rate_per_sqft"])
    _df["location_key"] = _df["location"].fillna("").astype(str).str.strip().str.casefold()
    _df["rate_per_sqft"] = pd.to_numeric(_df["rate_per_sqft"], errors="coerce")
    # Remove non-positive and implausibly large rates before computing medians.
    _valid_rates = _df.loc[_df["rate_per_sqft"].between(500, 100000)]
    _location_rates = _valid_rates.groupby("location_key")["rate_per_sqft"].median().to_dict()
    GLOBAL_MEDIAN_RATE = float(_valid_rates["rate_per_sqft"].median()) if not _valid_rates.empty else 6111.0
except Exception:
    app.logger.exception("Could not load rate lookup from dataset.csv; using global median.")
    _location_rates = {}
    GLOBAL_MEDIAN_RATE = 6111.0


def resolve_location(user_input: str):
    """Accept only an exact supported locality (case-insensitive, trimmed)."""
    value = re.sub(r"\s+", " ", (user_input or "").strip()).casefold()
    if not value:
        raise ValueError("Please enter an Ahmedabad area or location.")

    normalized = {re.sub(r"\s+", " ", loc.strip()).casefold(): loc for loc in locations}
    if value in normalized:
        return normalized[value], False

    raise ValueError(
        "Invalid location. This locality is not in the supported Ahmedabad dataset. "
        "Please enter a supported area such as Satellite or Bopal."
    )


def median_rate_for(location: str) -> float:
    return float(_location_rates.get(location.strip().casefold(), GLOBAL_MEDIAN_RATE))


def format_crore(value: float) -> str:
    if not np.isfinite(value) or value <= 0:
        raise ValueError("The model returned an invalid estimate. Please review the inputs.")
    if value < 1:
        return f"₹{value * 100:.1f} lakh"
    return f"₹{value:.2f} crore"


def render_page(prediction=None, error=None, matched_location=None, rate_used=None):
    return render_template(
        "index.html",
        locations=locations,
        area_types=area_types,
        property_types=property_types,
        prediction_text=prediction,
        error_text=error,
        matched_location=matched_location,
        rate_used=round(rate_used) if rate_used is not None else None,
    )


@app.get("/")
def home():
    return render_page()


@app.get("/health")
def health():
    return {"status": "ok", "service": "Intel Estate", "model_loaded": model is not None}


@app.post("/predict")
def predict():
    try:
        location_input = request.form.get("location", "")
        area_type = request.form.get("area_type", "").strip().casefold()
        property_type = request.form.get("property_type", "").strip().casefold()
        sqft_raw = request.form.get("sqft", "").strip()
        bhk_raw = request.form.get("bhk_type", "").strip()

        if not sqft_raw or not bhk_raw:
            raise ValueError("Enter both the total area and BHK count.")
        try:
            sqft = float(sqft_raw)
            bhk = int(bhk_raw)
        except (TypeError, ValueError):
            raise ValueError("Area must be numeric and BHK must be a whole number.")
        if not np.isfinite(sqft) or not 100 <= sqft <= 100000:
            raise ValueError("Area must be between 100 and 100,000 square feet.")
        if not 1 <= bhk <= 10:
            raise ValueError("BHK must be between 1 and 10.")

        area_lookup = {item.casefold(): item for item in area_types}
        property_lookup = {item.casefold(): item for item in property_types}
        if area_type not in area_lookup:
            raise ValueError("Please select a supported area type.")
        if property_type not in property_lookup:
            raise ValueError("Please select a supported property type.")

        location, was_matched = resolve_location(location_input)
        rate = median_rate_for(location)
        loc_code = int(location_encoder.transform([location])[0])
        area_code = int(area_encoder.transform([area_lookup[area_type]])[0])
        property_code = int(property_encoder.transform([property_lookup[property_type]])[0])

        # Keep the same feature order used to train model.pkl. Do not apply a
        # second hand-written BHK multiplier: BHK is already a model feature.
        features = pd.DataFrame([[loc_code, sqft, rate, area_code, property_code, bhk]], columns=[
            "location", "area_in_sqft", "rate_per_sqft", "area_type", "property_type", "bhk_type"
        ])
        predicted_crore = float(model.predict(features)[0])
        if not np.isfinite(predicted_crore) or predicted_crore <= 0:
            raise ValueError("The model could not produce a valid estimate for these inputs.")

        return render_page(
            prediction=format_crore(predicted_crore),
            matched_location=location,
            rate_used=rate,
        )
    except ValueError as exc:
        return render_page(error=str(exc)), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return render_page(error="Something went wrong while estimating the price. Check the inputs and try again."), 500


if __name__ == "__main__":
    # Debug is off by default so the interactive debugger is not exposed.
    app.run(host="127.0.0.1", port=5000, debug=False)
