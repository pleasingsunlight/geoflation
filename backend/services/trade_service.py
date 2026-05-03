from backend.models.schemas import TradeNode, TradeEdge, TradeNetworkResponse
from datetime import datetime, timedelta
import random
from backend.models.schemas import CommodityPoint, CommoditySeries, CommodityTrendsResponse
from backend.ml_models.price_forecast import forecast_commodity



def get_trade_network() -> TradeNetworkResponse:
    """
    Mock trade network (will later be replaced with real data / graph model)
    """

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

    return TradeNetworkResponse(nodes=nodes, edges=edges)


def get_commodity_trends() -> CommodityTrendsResponse:
    oil = forecast_commodity(80)
    gas = forecast_commodity(50)
    wheat = forecast_commodity(30)

    return CommodityTrendsResponse(trends=[
        CommoditySeries(commodity="oil", data=oil),
        CommoditySeries(commodity="gas", data=gas),
        CommoditySeries(commodity="wheat", data=wheat),
    ])