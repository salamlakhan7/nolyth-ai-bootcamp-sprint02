# Titanic Survival Prediction

Sprint 02 official project - Nolyth AI Bootcamp (Associate AI Engineer Training Program).

**Live app:** https://titanic-survival-predictor-2026.streamlit.app

**Backend API:** https://titanic-survival-prediction-ajac.onrender.com/docs

## Project Objective

Predict whether a passenger survived the Titanic disaster, based on passenger data (class, age, sex, fare, family size, etc.), using classification models built in Sprint 02 — then serve those models through a real, deployed full-stack application with user authentication and prediction history.

## Why Titanic

- One of the most well-documented datasets in machine learning — extensive reference material available
- Genuine feature engineering opportunity (extracting `Title` from `Name`, building `FamilySize` from `SibSp` + `Parch`)
- Real, meaningful missing data (`Age`, `Cabin`, `Embarked`) requiring real cleaning decisions
- Small enough to reason about every row, rich enough (numeric + categorical mix) to demonstrate real preprocessing skill

## Dataset

Source: [Kaggle - Titanic: Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic)

- `train.csv` — 891 rows, includes the `Survived` target column
- Columns: `PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked`

## Models

- **Logistic Regression** : simple, interpretable baseline (Accuracy 0.799, AUC 0.837)
- **Random Forest** : stronger, non-linear comparison model (Accuracy 0.793, AUC 0.836)

Both models perform similarly overall, but differ in tradeoff: Logistic Regression favors recall, Random Forest favors precision. Random Forest's feature importance confirms `Sex` as the dominant predictor, consistent with EDA findings, followed by `Fare`, `Age`, and `Pclass`.

## Data Science Workflow (Google Colab)

1. **Data loading and inspection** : shape, types, missing values
2. **Data cleaning** : dropped `PassengerId`/`Ticket`; imputed `Age` using per-`Title` median (not a flat median, since "Master" and "Mr" have very different real ages); converted `Cabin` into a `HasCabin` binary flag (77% missing, too sparse to impute directly); filled the 2 missing `Embarked` rows with the mode
3. **Feature engineering** : extracted `Title` from `Name` (grouped into Mr/Miss/Mrs/Master/Rare), built `FamilySize` from `SibSp` + `Parch`
4. **Encoding** : `Sex` binary-encoded; `Embarked` and `Title` one-hot encoded; dropped `Title_Mr` to resolve multicollinearity with `Sex` (correlation of -0.87)
5. **EDA** : 4 charts (survival by sex, survival by class, age distribution by survival, correlation heatmap) with written insights
6. **Train/test split** : stratified, to preserve the ~38% survival rate in both sets
7. **Model training** : Logistic Regression (scaled features) and Random Forest (raw features)
8. **Evaluation** : accuracy, confusion matrix, precision/recall/F1, AUC, feature importance
9. **Model saving** : `joblib.dump()` for both models plus the `StandardScaler`, downloaded and committed to this repo

Full notebook: [`titanic_model_training.ipynb`](./titanic_model_training.ipynb)

## Application Architecture

```
┌─────────────────────┐         ┌──────────────────────────┐         ┌──────────────┐
│  Streamlit Frontend  │ ──────► │   FastAPI Backend         │ ──────► │  Neon (Postgres) │
│  (Streamlit Cloud)   │  HTTP   │   (Render)                │  SQL    │  titanic_db      │
└─────────────────────┘         └──────────────────────────┘         └──────────────┘
                                          │
                                          ▼
                                 backend/models/*.pkl
                                 (Logistic Regression,
                                  Random Forest, Scaler)
```

**Backend (FastAPI):**
- `POST /register`, `POST /login` : user auth with hashed passwords (bcrypt) and JWT tokens
- `POST /predict` : accepts passenger details, runs both models, returns predictions + probabilities, logs the result to the database
- `GET /history` : returns the logged-in user's past predictions
- Database: Neon Postgres, via SQLAlchemy (`User` and `PredictionHistory` tables)

**Frontend (Streamlit):**
- Login / Register tabs
- Passenger detail input form → calls `/predict` → shows both models' results side by side
- History tab → calls `/history` → shows past predictions in a table
- Retry-with-backoff logic on every backend call, to gracefully handle the backend's free-tier cold start (see Deployment Notes below)

## Deployment

- **Backend:** Render (free tier), environment variables (`DATABASE_URL`, `SECRET_KEY`) set as Render secrets
- **Frontend:** Streamlit Community Cloud (free tier)
- **Database:** Neon, a separate `titanic_db` database created within the existing Neon project (isolated from the Sprint 01 database)

### Real issues hit and fixed during deployment

- **bcrypt/passlib incompatibility** : newer `bcrypt` (4.1+) removed an attribute `passlib` expects, causing password hashing to fail. Fixed by pinning `bcrypt==4.0.1`.
- **Neon SSL connection drops** : pooled connections were being silently closed by Neon, causing `SSL connection has been closed unexpectedly` errors. Fixed by adding `pool_pre_ping=True` to the SQLAlchemy engine, so dead connections are detected and replaced automatically.
- **`.env` loading failures** : `export $(cat .env | xargs)` broke on a connection string containing `&` (interpreted by bash as a background-job operator). Fixed by quoting the value and switching to `source .env` with `set -a` / `set +a`.
- **Render cold starts causing `ConnectionError`** : Render's free tier fully shuts down the backend after ~15 minutes of inactivity; the first request after that can fail outright while the container is still booting (not just "slow"). Fixed with retry-with-backoff logic in the frontend (5 retries, 5s apart, 90s timeout per attempt), plus a `st.spinner()` so the wait is visible rather than looking broken.

## Local Testing

Both backend and frontend were fully tested locally (two terminals, backend on `localhost:8000`, frontend via `streamlit run`) before deployment, using FastAPI's Swagger UI (`/docs`) to verify each endpoint individually (register → login → authorize → predict → history) against the real Neon database, before testing the same flow through the actual Streamlit UI.

## Screenshots

| # | Screenshot | What it verifies |
|---|---|---|
| 01 | `01_api_root_running.png` | Backend root endpoint responding locally |
| 02 | `02_swagger_docs_page.JPG` | FastAPI interactive docs loaded, all endpoints visible |
| 03 | `03_register_success.JPG` | `/register` — user creation working against Neon |
| 04 | `04_login_success.JPG` | `/login` — JWT token issued successfully |
| 05 | `05_predict_response.JPG` | `/predict` — real model output returned |
| 06 | `06_history_response.JPG` | `/history` — prediction correctly logged and retrieved |
| 07 | `07_get_root_run_successful_with_response.JPG` | Root endpoint re-verified after fixes |
| 08 | `08_frontend_predict_form.JPG` | Streamlit UI — passenger input form, logged in |
| 09 | `09_frontend_prediction_result.JPG` | Streamlit UI — prediction results displayed |
| 10 | `10_frontend_history_tab.JPG` | Streamlit UI — history tab showing past predictions |
| 11 | `11_Successful_render_deployed_showdocs.JPG` | Backend live on Render, `/docs` reachable publicly |
| 12 | `12_frontend_live_deployed.JPG` | Full app live and working on Streamlit Community Cloud |

## Repo Structure

```
Titanic-Survival-Prediction/
├── README.md
├── titanic_model_training.ipynb
├── logistic_regression_titanic.pkl
├── random_forest_titanic.pkl
├── scaler_titanic.pkl
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models_db.py
│   ├── schemas.py
│   ├── auth.py
│   ├── ml_model.py
│   ├── requirements.txt
│   └── models/
│       ├── logistic_regression_titanic.pkl
│       ├── random_forest_titanic.pkl
│       └── scaler_titanic.pkl
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── Dockerfile
├── start.sh
├── SETUP.md
└── screenshots/
```

## What's Next

- Clustering models (K-Means, Hierarchical, DBSCAN) - remaining Sprint 02 ML topics, not used in this project but part of the sprint curriculum
- Full manual (pen-and-paper) revision pass of everything covered in Sprint 02, ahead of the viva
- Optional: a second backend deployment on Hugging Face Spaces (Docker, combined backend+frontend), as an alternative to Render

---
*Nolyth AI Bootcamp Sprint 02 - Titanic Survival Prediction - complete and deployed.*
