from backend.models.schemas import TradeNode, TradeEdge, TradeNetworkResponse
from datetime import datetime, timedelta
import random
from backend.models.schemas import CommodityPoint, CommoditySeries, CommodityTrendsResponse
from backend.ml_models.price_forecast import forecast_commodity
from backend.utils.cache import get_cache, set_cache


def get_trade_network() -> TradeNetworkResponse:
    """
    Mock trade network (cached)
    """

    # Try cache first
    cached = get_cache("trade_network")
    if cached:
        return TradeNetworkResponse(**cached)

    # Build network
    nodes = [
        TradeNode(id="russia", name="Russia", type="country"),
        TradeNode(id="china", name="China", type="country"),
        TradeNode(id="eu", name="European Union", type="country"),
        TradeNode(id="oil", name="Oil", type="commodity"),
    ]

    edges = [
        TradeEdge(source="russia", target="eu", weight=0.9),
        TradeEdge(source="russia", target="china", weight=0.7),
        TradeEdge(source="oil", target="eu", weight=0.8),
    ]

    network = {
        "nodes": [node.dict() for node in nodes],
        "edges": [edge.dict() for edge in edges],
    }

    # Store in cache
    set_cache("trade_network", network)

    return TradeNetworkResponse(**network)


def get_commodity_trends() -> CommodityTrendsResponse:
    cached = get_cache("commodity_trends")

    if cached:
        return cached

    oil = forecast_commodity(80)
    gas = forecast_commodity(50)
    wheat = forecast_commodity(30)

    result = {
        "trends": [
            {"commodity": "oil", "data": oil},
            {"commodity": "gas", "data": gas},
            {"commodity": "wheat", "data": wheat},
        ]
    }

    set_cache("commodity_trends", result)

    return result