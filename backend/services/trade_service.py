from backend.models.schemas import TradeNode, TradeEdge, TradeNetworkResponse
from datetime import datetime, timedelta
import random
from backend.models.schemas import CommodityPoint, CommoditySeries, CommodityTrendsResponse
from backend.ml_models.price_forecast import forecast_commodity
from backend.utils.cache import get_cache, set_cache


from backend.data_pipeline.load_trade_network import (
    load_trade_network
)


def get_trade_network():
    cached = get_cache(
        "trade_network"
    )

    if cached:
        return cached

    graph, df = load_trade_network()

    nodes = [
        {
            "id": node,
            "name": node,
            "type": "country"
        }
        for node in graph.nodes()
    ]

    edges = [
        {
            "source": row["source"],
            "target": row["target"],
            "weight": row["weight"]
        }
        for _, row in df.iterrows()
    ]

    result = {
        "nodes": nodes,
        "edges": edges
    }

    set_cache(
        "trade_network",
        result
    )

    return result


def get_commodity_trends():
    cached = get_cache(
        "commodity_trends"
    )

    if cached:
        return cached

    oil = forecast_commodity("oil")
    gas = forecast_commodity("gas")
    wheat = forecast_commodity("wheat")

    result = {
        "trends": [
            {
                "commodity": "oil",
                "data": oil
            },
            {
                "commodity": "gas",
                "data": gas
            },
            {
                "commodity": "wheat",
                "data": wheat
            }
        ]
    }

    set_cache(
        "commodity_trends",
        result
    )

    return result