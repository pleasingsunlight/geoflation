from collections import deque

from backend.data_pipeline.load_trade_network import (
    load_trade_network
)


DECAY_FACTOR = 0.6
MAX_DEPTH = 3


def propagate_trade_shock(
    source_country,
    severity
):
    graph, _ = load_trade_network()

    impacted = {}

    if source_country not in graph:
        return impacted

    queue = deque()

    queue.append(
        (
            source_country,
            severity,
            0
        )
    )

    visited = set()

    while queue:
        current, current_severity, depth = queue.popleft()

        if depth >= MAX_DEPTH:
            continue

        if current in visited:
            continue

        visited.add(current)

        neighbors = graph[current]

        for neighbor in neighbors:
            edge_data = graph[current][neighbor]

            weight = edge_data.get(
                "weight",
                1
            )

            propagated_impact = round(
                current_severity
                * (weight / 100)
                * (DECAY_FACTOR ** depth),
                2
            )

            existing = impacted.get(
                neighbor,
                0
            )

            impacted[neighbor] = max(
                existing,
                propagated_impact
            )

            queue.append(
                (
                    neighbor,
                    propagated_impact,
                    depth + 1
                )
            )

    return impacted