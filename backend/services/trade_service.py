from backend.models.schemas import TradeNode, TradeEdge, TradeNetworkResponse
from datetime import datetime, timedelta
import random
from backend.models.schemas import CommodityPoint, CommoditySeries, CommodityTrendsResponse



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
    """
    Mock time-series data (simulates forecast output)
    """

    base_date = datetime.now()

    def generate_series(name, base_price):
        data = []
        for i in range(10):
            date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
            price = base_price + random.uniform(-5, 5)
            data.append(CommodityPoint(date=date, price=round(price, 2)))
        return CommoditySeries(commodity=name, data=data)

    trends = [
        generate_series("oil", 80),
        generate_series("gas", 50),
        generate_series("wheat", 30),
    ]

    return CommodityTrendsResponse(trends=trends)