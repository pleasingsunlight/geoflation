from fastapi import APIRouter
from backend.models.schemas import CommodityTrendsResponse
from backend.services.trade_service import get_commodity_trends

router = APIRouter()


@router.get("/commodity-trends", response_model=CommodityTrendsResponse)
def commodity_trends():
    return get_commodity_trends()