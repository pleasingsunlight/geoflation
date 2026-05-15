from backend.data_pipeline.load_trade_network import (
    load_trade_network
)


def propagate_trade_shock(
    source_country,
    severity
):
    graph, _ = load_trade_network()

    impacted = {}

    if source_country not in graph:
        return impacted

    neighbors = graph[source_country]

    for neighbor in neighbors:
        edge_data = graph[source_country][neighbor]

        weight = edge_data.get(
            "weight",
            1
        )

        impact_score = round(
            severity * (weight / 100),
            2
        )

        impacted[neighbor] = impact_score

    return impacted