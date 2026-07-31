from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PassengerInput(BaseModel):
    pclass: int          # 1, 2, or 3
    sex: int             # 0 = male, 1 = female
    age: float
    fare: float
    family_size: int     # SibSp + Parch + 1
    has_cabin: int        # 0 or 1
    embarked: str         # "C", "Q", or "S"
    title: str            # "Mr", "Miss", "Mrs", "Master", "Rare"


class PredictionResult(BaseModel):
    logistic_prediction: int
    logistic_probability: float
    rf_prediction: int
    rf_probability: float


class HistoryItem(BaseModel):
    id: int
    pclass: int
    sex: int
    age: float
    fare: float
    family_size: int
    has_cabin: int
    embarked: str
    title: str
    logistic_prediction: int
    logistic_probability: float
    rf_prediction: int
    rf_probability: float
    created_at: datetime

    class Config:
        from_attributes = True