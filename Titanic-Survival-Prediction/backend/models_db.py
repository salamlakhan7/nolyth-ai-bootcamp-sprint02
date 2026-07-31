from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("PredictionHistory", back_populates="user")


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # input features
    pclass = Column(Integer)
    sex = Column(Integer)
    age = Column(Float)
    fare = Column(Float)
    family_size = Column(Integer)
    has_cabin = Column(Integer)
    embarked = Column(String)
    title = Column(String)

    # results
    logistic_prediction = Column(Integer)
    logistic_probability = Column(Float)
    rf_prediction = Column(Integer)
    rf_probability = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="predictions")