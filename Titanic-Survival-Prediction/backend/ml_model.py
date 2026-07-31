import joblib
import pandas as pd
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

log_model = joblib.load(os.path.join(MODEL_DIR, "logistic_regression_titanic.pkl"))
rf_model = joblib.load(os.path.join(MODEL_DIR, "random_forest_titanic.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler_titanic.pkl"))

# Must match the exact column order used during training in Colab
FEATURE_COLUMNS = [
    "Pclass", "Sex", "Age", "Fare", "HasCabin", "FamilySize",
    "Embarked_Q", "Embarked_S",
    "Title_Miss", "Title_Mrs", "Title_Rare",
]


def build_feature_row(passenger: dict) -> pd.DataFrame:
    """Convert raw passenger input into the one-hot encoded row the models expect."""
    row = {col: 0 for col in FEATURE_COLUMNS}

    row["Pclass"] = passenger["pclass"]
    row["Sex"] = passenger["sex"]
    row["Age"] = passenger["age"]
    row["Fare"] = passenger["fare"]
    row["HasCabin"] = passenger["has_cabin"]
    row["FamilySize"] = passenger["family_size"]

    embarked = passenger["embarked"]
    if embarked == "Q":
        row["Embarked_Q"] = 1
    elif embarked == "S":
        row["Embarked_S"] = 1
    # "C" -> both stay 0 (it was the dropped baseline category)

    title = passenger["title"]
    if title in ("Miss", "Mrs", "Rare"):
        row[f"Title_{title}"] = 1
    # "Mr" and "Master" -> all Title_ columns stay 0
    # (Title_Mr was dropped during training; Master has no dummy column either)

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def predict(passenger: dict) -> dict:
    X = build_feature_row(passenger)
    X_scaled = scaler.transform(X)

    log_pred = int(log_model.predict(X_scaled)[0])
    log_proba = float(log_model.predict_proba(X_scaled)[0][1])

    rf_pred = int(rf_model.predict(X)[0])
    rf_proba = float(rf_model.predict_proba(X)[0][1])

    return {
        "logistic_prediction": log_pred,
        "logistic_probability": round(log_proba, 4),
        "rf_prediction": rf_pred,
        "rf_probability": round(rf_proba, 4),
    }