# Intel Estate — Ahmedabad Property Valuation

Intel Estate is a Flask-based machine-learning prototype that estimates a property's indicative value from its location, area, area type, property type, and BHK count. It uses a saved Random Forest regression model trained on historical Ahmedabad property-listing data.

> **Important:** This is an educational estimate, not a formal valuation, appraisal, offer, or guarantee of market price. Listing data may be incomplete or outdated.

## Features

- Responsive, neo-brutalist interface.
- Location matching with conservative fuzzy matching; unsupported locations produce a validation message rather than silently mapping to an unrelated location.
- Input validation for area, BHK, and categorical selections.
- Uses a location-specific median `rate_per_sqft` from `dataset.csv` where available, with a filtered dataset-wide median as fallback.
- Displays the matched dataset location and rate feature used.
- Safe output rendering (no `safe` filter on user/model output), generic user-facing errors, and server-side logging.
- `/health` endpoint for a basic service check.

## Project structure

```text
IntelEstate/
├── app.py
├── model.pkl
├── location_encoder.pkl
├── area_encoder.pkl
├── property_encoder.pkl
├── dataset.csv
├── requirements.txt
├── README.md
├── evaluate_model.py
├── tests/
│   └── test_app.py
└── templates/
    └── index.html
```

## Requirements

- Python 3.11 recommended.
- The saved model was serialized with scikit-learn 1.8.0; keep the pinned version to reduce pickle compatibility issues.
- About 150 MB of disk space for the model and dataset, plus installed dependencies.

## Run locally (Windows PowerShell)

1. Extract the ZIP and open PowerShell in the folder containing `app.py`.
2. Create a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Start the app:

   ```powershell
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser. Visit `http://127.0.0.1:5000/health` to check the service.

## Run locally (macOS/Linux)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## Model behavior and limitations

- The model expects the following feature order: `location`, `area_in_sqft`, `rate_per_sqft`, `area_type`, `property_type`, `bhk_type`.
- The target is `price_in_cr` (crores). The application therefore does not convert the model result from rupees or add a hand-written BHK multiplier.
- The app no longer invents a ±10% range. It reports a point estimate because a calibrated prediction interval has not yet been established.
- The dataset has missing values and outliers. Model quality should be reported only from a held-out evaluation, not from predictions on training rows. A fresh held-out evaluation with `evaluate_model.py` returned R² = **0.9670**, MAE = **0.0659 crore** (about ₹6.59 lakh), and RMSE = **0.2570 crore** (about ₹25.70 lakh) on 3,827 test rows in this environment. Run `python evaluate_model.py` to reproduce the evaluation; results may vary if the data or library versions change.
- `rate_per_sqft` is approximated with historical median data at prediction time. The result depends on the quality and granularity of location data and should be validated before any real-world use.

## Security and deployment notes

- The local development server binds to `127.0.0.1` and debug mode is disabled.
- For public deployment, use a production WSGI server (for example, Waitress on Windows or Gunicorn on Linux), configure a reverse proxy/HTTPS, add request logging and rate limiting, and avoid exposing detailed exceptions to users.
- Do not commit virtual environments, private data, or generated secrets to source control.


### Location validation fix
Unknown or unrelated locations are rejected with an on-page error instead of being
silently mapped to another locality. Exact names and unique partial locality names
of at least four characters are accepted. The regression test includes the reported
invalid input `dijik astra`.


### Form validation message behavior
An error from a previous submission is hidden immediately when the user edits any form field.
The next submission shows the fresh server response: a new validation error for invalid input,
or a prediction for a supported locality.
