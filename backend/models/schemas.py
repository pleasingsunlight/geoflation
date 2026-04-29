from pydantic import BaseModel, Field
from typing import Dict, List
from enum import Enum


class EventType(str, Enum):
    sanction = "sanction"
    war = "war"
    tariff = "tariff"
    port_closure = "port_closure"


class Sector(str, Enum):
    energy = "energy"
    technology = "technology"
    manufacturing = "manufacturing"
    trade = "trade"
    general = "general"


class EventInput(BaseModel):
    event_type: EventType
    country: str = Field(..., min_length=2, max_length=50)
    sector: Sector
    severity: float = Field(..., ge=0.0, le=1.0)


class PredictionResponse(BaseModel):
    price_impacts: Dict[str, str]
    shipping_delay_weeks: int
    affected_industries: List[str]
    risk_severity: str