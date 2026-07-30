# Titanic Survival Prediction

Sprint 02 official project - Nolyth AI Bootcamp (Associate AI Engineer Training Program).

## Project Objective

Predict whether a passenger survived the Titanic disaster, based on passenger data (class, age, sex, fare, family size, etc.), using classification models learned throughout Sprint 02.

## Why Titanic

- One of the most well-documented datasets in machine learning — extensive reference material available
- Genuine feature engineering opportunity (e.g. extracting `Title` from `Name`, building `FamilySize` from `SibSp` + `Parch`)
- Real, meaningful missing data (`Age`, `Cabin`, `Embarked`) requiring real cleaning decisions
- Small enough to reason about every row, rich enough (numeric + categorical mix) to demonstrate real preprocessing skill

## Dataset

Source: [Kaggle - Titanic: Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic)

- `train.csv` — 891 rows, includes the `Survived` target column
- Columns: `PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked`

## Models

Baseline models (minimum 2, as required):

- **Logistic Regression** — simple, interpretable baseline
- **Random Forest** — stronger, non-linear comparison model

(Decision Tree may be added as a third model for additional depth.)

## Workflow

1. Data loading and inspection
2. Data cleaning (missing values, data types)
3. Feature engineering (Title, FamilySize, encoding)
4. Exploratory Data Analysis (4+ charts with written insights)
5. Model training (Logistic Regression, Random Forest)
6. Evaluation (accuracy, confusion matrix, precision/recall/F1)
7. Model saving (`joblib`/`pickle`) for later use in a FastAPI + Streamlit app

## Planned Extension

A FastAPI backend + Streamlit frontend (similar in shape to Sprint 01), where a user registers/logs in, explores the Titanic dataset, and views model prediction results.

## Development Notes

Initial model training and experimentation done in Google Colab (to conserve Codespaces usage). Trained models saved and brought back into this repo / Codespace for the backend + frontend build.

---
*Nolyth AI Bootcamp Sprint 02 — Titanic Survival Prediction — in progress.*
