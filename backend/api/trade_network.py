from fastapi import APIRouter
from backend.models.schemas import TradeNetworkResponse
from backend.services.trade_service import get_trade_network

router = APIRouter()


@router.get("/trade-network", response_model=TradeNetworkResponse)
def trade_network():
    return get_trade_network()