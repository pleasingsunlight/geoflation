"""
trade_propagation.py

Shock propagation over the real UN Comtrade trade graph.
"""

from __future__ import annotations

from backend.graph.graph_loader import load_trade_graph


_GRAPH = None


def _get_graph():
    """
    Lazy-load the trade graph.
    """

    global _GRAPH

    if _GRAPH is None:
        _GRAPH = load_trade_graph()

    return _GRAPH


def propagate_trade_shock(
    source_country: str,
    severity: float,
    max_neighbors: int = 10,
):
    """
    Propagate a geopolitical shock through the trade graph.

    Returns
    -------
    dict

    {
        "CHN":0.82,
        "USA":0.55,
        ...
    }
    """

    graph = _get_graph()

    if source_country not in graph:
        raise ValueError(
            f"{source_country} not present in trade graph."
        )

    edges = []

    total_trade = 0.0

    for _, target, data in graph.out_edges(
        source_country,
        data=True
    ):

        trade_value = float(
            data.get(
                "total_trade_value",
                0.0
            )
        )

        if trade_value <= 0:
            continue

        total_trade += trade_value

        edges.append(
            (
                target,
                trade_value
            )
        )

    if total_trade == 0:

        return {}

    impacts = {}

    for target, trade_value in edges:

        score = (
            trade_value
            / total_trade
        ) * severity

        impacts[target] = round(
            score,
            4
        )

    impacts = dict(

        sorted(
            impacts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_neighbors]

    )

    return impacts


if __name__ == "__main__":

    impacts = propagate_trade_shock(
        "USA",
        severity=0.8
    )

    print()

    print("Propagation Result")

    print("-" * 60)

    for country, score in impacts.items():
        print(
            f"{country:>5} : {score:.4f}"
        )