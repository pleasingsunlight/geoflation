from pydantic import BaseModel
from typing import Dict, List


class EventInput(BaseModel):
    event_type: str
    country: str
    sector: str
    severity: float


class PredictionResponse(BaseModel):
    price_impacts: Dict[str, str]
    shipping_delay_weeks: int
    affected_industries: List[str]
    risk_severity: str