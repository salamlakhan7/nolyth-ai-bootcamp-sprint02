# Nolyth AI Bootcamp - Sprint 02: Data Analysis & Machine Learning

This repository documents my work through **Sprint 02** of the Nolyth AI Bootcamp (Associate AI Engineer Training Program) - turning raw datasets into insights and working machine learning models, then shipping one of them as a real, deployed application.

The sprint covers the full classical ML stack: NumPy, Pandas, EDA and visualization, Regression, Classification, Clustering, and model evaluation - backed by a production build with a FastAPI backend, a Neon Postgres database, and a Streamlit frontend, deployed live.

## Program Info

**Program:** Nolyth AI Bootcamp - Associate AI Engineer Training
**Sprint:** 02 - Data Analysis & Machine Learning
**Duration:** 2 Weeks (Days 1-14)
**Stack:** Python, NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, Jupyter/Colab, FastAPI, SQLAlchemy, Neon (Postgres), Streamlit, Render, Streamlit Community Cloud

## Sprint Project - Titanic Survival Prediction

**Live app:** https://titanic-survival-predictor-2026.streamlit.app
**Backend API:** https://titanic-survival-prediction-ajac.onrender.com/docs
**Details:** [`Titanic-Survival-Prediction/README.md`](./Titanic-Survival-Prediction/README.md)

A classification model - Logistic Regression and Random Forest, compared side by side - predicting Titanic passenger survival, served through a real deployed application: user registration and login, a prediction interface, and persisted prediction history, backed by a Postgres database.

### Why the project changed from the original plan

Sprint 02 originally targeted **Customer Churn Prediction** on the Telco dataset, and a full EDA + Logistic Regression baseline was built against it early on. After working through all five classification models (Logistic Regression, Decision Tree, Random Forest, KNN, SVM) in depth, classification was clearly the stronger area - and Titanic offered a cleaner opportunity to demonstrate real feature engineering (`Title` extraction, `FamilySize` construction) and a full deployment, rather than staying in notebook-only territory. The churn EDA and Logistic Regression work remain in this repo as part of the classification practice; Titanic is the shipped deliverable.

## What This Repo Covers

| Area | What Was Practiced | Where |
|---|---|---|
| Data Analysis Tools | NumPy arrays, numerical operations, Pandas Series/DataFrames, CSV loading, data inspection | `notebooks/` |
| Data Cleaning | Missing values, duplicates, type conversion, filtering, grouping, feature creation | `notebooks/`, `Titanic-Survival-Prediction/` |
| EDA + Visualization | Patterns, trends, outliers, correlations; bar charts, histograms, scatter plots, heatmaps | `notebooks/`, `visuals/` |
| Regression | Linear, Polynomial, Non-linear — theory, manual derivations, and real datasets (California Housing, Kaggle Position Salaries, Telco tenure/charges) | `Regressions/` |
| Classification | Logistic Regression, Decision Tree, Random Forest, KNN, SVM — theory, math breakdowns, real dataset runs (Telco, Breast Cancer Wisconsin), full evaluation | `Classification/` |
| Clustering | K-Means, Hierarchical Clustering, DBSCAN | in progress |
| Applied ML → Production | Trained models served through a real backend, database, and deployed frontend | `Titanic-Survival-Prediction/` |

## Minimum Functional Requirements

- Dataset loading and clear problem statement
- Data cleaning and preprocessing steps
- EDA with at least 4 meaningful charts
- Written insights, not only visual outputs
- At least 2 ML models with baseline comparison (this repo ships 5 classification models, well past the minimum)
- Train/test split and evaluation metrics
- GitHub repository with README, setup steps, and screenshots
- Short demo explaining dataset, approach, results, and limitations
- **Beyond the minimum:** a deployed, working application — not just a notebook — with real authentication, a real database, and public URLs

## Repo Structure

```
.
├── Regressions/                    Linear, Polynomial, Non-linear Regression — theory + practice
├── Classification/                 Logistic Regression, Decision Tree, Random Forest, KNN, SVM
├── Titanic-Survival-Prediction/    Final project: model training + deployed FastAPI/Streamlit app
├── notebooks/                      Early NumPy / Pandas / Matplotlib / Seaborn practice
├── data/                           Raw and cleaned dataset files
├── visuals/                        Exported charts and screenshots
└── README.md                       This file
```

## Engineering Practices Followed

- **Incremental commits** — one stage (cleaning → EDA → modeling → evaluation) → one commit → push → next stage, carried over from the Sprint 01 workflow
- **Environment isolation** — separate Neon database per project (`titanic_db`, isolated from the Sprint 01 database), secrets managed via platform environment variables, not committed to source control
- **Local-before-deploy testing** — every endpoint verified locally against a real database via FastAPI's Swagger UI before any deployment attempt
- **Real production debugging** — dependency version conflicts (bcrypt/passlib), connection pooling failures (Neon SSL drops), and free-tier cold-start handling (retry-with-backoff logic) were all encountered and fixed, not avoided by picking a simpler stack
- **Documented incident response** — an accidental credential leak (`.env` pushed to a public repo) was caught, and handled by rotating the exposed credentials and removing the file, rather than left unaddressed

## What's Next

- Complete Clustering (K-Means, Hierarchical, DBSCAN) — the remaining Sprint 02 ML topic
- Full manual, pen-and-paper revision pass of every model covered this sprint, ahead of the viva
- Optional: a second backend deployment on Hugging Face Spaces, as an alternative to Render

---
*Nolyth AI Bootcamp Sprint 02 — Regression, Classification, and a deployed ML application, shipped.*
