from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
import models_db
import schemas
import auth
import ml_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Titanic Survival Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Streamlit app's URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models_db.User).filter(models_db.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models_db.User(
        username=user.username,
        hashed_password=auth.hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models_db.User).filter(models_db.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/predict", response_model=schemas.PredictionResult)
def predict(
    passenger: schemas.PassengerInput,
    db: Session = Depends(get_db),
    current_user: models_db.User = Depends(auth.get_current_user),
):
    result = ml_model.predict(passenger.dict())

    record = models_db.PredictionHistory(
        user_id=current_user.id,
        pclass=passenger.pclass,
        sex=passenger.sex,
        age=passenger.age,
        fare=passenger.fare,
        family_size=passenger.family_size,
        has_cabin=passenger.has_cabin,
        embarked=passenger.embarked,
        title=passenger.title,
        logistic_prediction=result["logistic_prediction"],
        logistic_probability=result["logistic_probability"],
        rf_prediction=result["rf_prediction"],
        rf_probability=result["rf_probability"],
    )
    db.add(record)
    db.commit()

    return result


@app.get("/history", response_model=List[schemas.HistoryItem])
def history(
    db: Session = Depends(get_db),
    current_user: models_db.User = Depends(auth.get_current_user),
):
    records = (
        db.query(models_db.PredictionHistory)
        .filter(models_db.PredictionHistory.user_id == current_user.id)
        .order_by(models_db.PredictionHistory.created_at.desc())
        .all()
    )
    return records


@app.get("/")
def root():
    return {"message": "Titanic Survival Prediction API is running"}