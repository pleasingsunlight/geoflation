from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    country = Column(String)
    sector = Column(String)
    severity = Column(Float)

    oil_impact = Column(String)
    gas_impact = Column(String)
    delay = Column(Integer)
    risk = Column(String)