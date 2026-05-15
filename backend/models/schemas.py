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
    impacted_countries: dict[str, float]
    affected_industries: List[str]
    risk_severity: str
    explanation: str


class TradeNode(BaseModel):
    id: str
    name: str
    type: str  # country / port / commodity


class TradeEdge(BaseModel):
    source: str
    target: str
    weight: float  # trade volume or dependency strength


class TradeNetworkResponse(BaseModel):
    nodes: List[TradeNode]
    edges: List[TradeEdge]

class CommodityPoint(BaseModel):
    date: str
    price: float


class CommoditySeries(BaseModel):
    commodity: str
    data: List[CommodityPoint]


class CommodityTrendsResponse(BaseModel):
    trends: List[CommoditySeries]