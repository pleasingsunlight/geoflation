from backend.models.schemas import TradeNode, TradeEdge, TradeNetworkResponse


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