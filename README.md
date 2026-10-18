# 🏡 IntelEstate

### AI-Powered House Price Prediction for Ahmedabad

**Estimate property prices using machine learning and a simple web
interface.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Academic%20Project-blue)](#)
:::

------------------------------------------------------------------------

## 📌 About the Project

**IntelEstate** is a machine-learning-based property price prediction
project focused on the Ahmedabad real-estate market. It uses property
information such as location, area, property type, area type, and BHK
configuration to estimate a property's price.

The project combines a trained regression model with a Flask web
application, allowing users to enter property details and view a
prediction through a browser.

> **Note:** Predictions are estimates based on the dataset and model
> used. They are not official property valuations or guarantees of
> current market prices.

## ✨ Key Features

-   **Property price estimation** using a machine-learning regression
    model.
-   **Ahmedabad-focused dataset** for location-aware estimation within
    the dataset's coverage.
-   **Web interface** built with HTML and CSS.
-   **Flask backend** to receive property details and return
    predictions.
-   **Categorical encoding** using saved encoders for supported input
    fields.
-   **Model evaluation** through a separate Python script for analysis
    and performance checks.

## 🧰 Technology Stack

  -----------------------------------------------------------------------
  Layer                               Tools
  ----------------------------------- -----------------------------------
  Programming language                Python

  Data processing                     Pandas, NumPy

  Machine learning                    Scikit-learn, Random Forest
                                      Regression

  Model and encoder persistence       Joblib, Pickle

  Backend                             Flask

  Frontend                            HTML, CSS

  Analysis and evaluation             `evaluate_model.py`, Matplotlib (if
                                      configured in the script)

  Version control                     Git, GitHub
  -----------------------------------------------------------------------

## 🔄 How It Works

1.  **Enter property details** --- provide the supported location and
    property attributes.
2.  **Validate and preprocess** --- the application checks inputs and
    converts categorical values using the saved encoders.
3.  **Generate a prediction** --- the trained regression model processes
    the prepared features.
4.  **Display the result** --- the Flask application returns the
    estimated price in the web interface.

``` text
User
  │
  ▼
HTML/CSS Form
  │
  ▼
Flask Application (app.py)
  │
  ▼
Input Validation & Encoding
  │
  ▼
Trained ML Model
  │
  ▼
Estimated Property Price
```

## 📁 Project Structure

``` text
IntelEstate/
├── app.py
├── dataset.csv
├── evaluate_model.py
├── location_encoder.pkl
├── area_encoder.pkl
├── property_encoder.pkl
├── requirements.txt
├── README.md
├── .gitignore
└── templates/
    └── index.html
```

The trained `model.pkl` file is not listed above because it may be
excluded from Git tracking due to its size. The application will need
the compatible model artifact at the path expected by `app.py`.

## ⚙️ Getting Started

### 1. Prerequisites

-   Python installed on your computer
-   Git (optional, for cloning the repository)
-   A compatible trained model file, if it is not included in the
    repository

### 2. Clone the repository

``` bash
git clone https://github.com/sahirparmar27/IntelEstate.git
cd IntelEstate
```

### 3. Create and activate a virtual environment

**Windows PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python
directly or follow your system's approved PowerShell execution-policy
guidance.

### 4. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Add the trained model artifact

If `model.pkl` is not included in the repository, place the compatible
file in the location expected by `app.py`. Check the model-loading path
near the top of `app.py` before running the application.

**Do not commit a large model file just to make the repository
complete.** If you choose to distribute it, use an appropriate release
or model-storage service and document how to obtain it.

### 6. Run the application

``` powershell
python app.py
```

Open the local address printed in the terminal (commonly
`http://127.0.0.1:5000`) in your browser.

## 📊 Model Evaluation

Use the evaluation script to review the project's model analysis:

``` powershell
python evaluate_model.py
```

The charts will appear only if the script includes plotting code and
calls the relevant display function. If you want to save charts for your
report, add `plt.savefig("filename.png", bbox_inches="tight")` before
`plt.show()` where appropriate.

An earlier project evaluation reported an **approximately 0.96 test R²
score**. Results may vary depending on the dataset, preprocessing,
train/test split, and model version. Run the current evaluation script
to confirm the metrics for the version you are using.

## 🗂️ Dataset and Responsible Use

The project uses property data associated with Ahmedabad. Before sharing
`dataset.csv` publicly, verify that you have permission to redistribute
it and that it contains no private or restricted information.

The quality of estimates depends on dataset coverage, data freshness,
feature preprocessing, and the model's evaluation methodology. The
system should be treated as an educational prototype rather than a
replacement for professional valuation.

## 🚀 Future Improvements

-   Add model versioning and reproducible training steps.
-   Report evaluation metrics such as MAE, RMSE, and R² in a consistent
    evaluation pipeline.
-   Improve validation for unknown or misspelled locations.
-   Add charts for location-wise price trends and feature importance.
-   Refresh the dataset periodically and evaluate performance on unseen
    data.
-   Deploy the application with secure configuration and clear
    model-artifact management.

## 👨‍💻 Author

**Sahir Parmar**\
B.Tech student in Artificial Intelligence

-   GitHub: [@sahirparmar27](https://github.com/sahirparmar27)
-   Repository:
    [IntelEstate](https://github.com/sahirparmar27/IntelEstate)

------------------------------------------------------------------------


**Built as a practical machine-learning project for real-estate price
estimation.**
