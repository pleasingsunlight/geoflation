"""
graph_statistics.py

Generate statistics for the trade graph.
"""

from pathlib import Path
import json
from datetime import datetime, UTC

import networkx as nx

from backend.graph.graph_loader import load_trade_graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "graph"
    / "graph_statistics.json"
)


def generate_statistics(graph: nx.DiGraph):

    total_trade = sum(
        d["total_trade_value"]
        for _, _, d in graph.edges(data=True)
    )

    exporters = sorted(
        graph.out_degree(weight="total_trade_value"),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    importers = sorted(
        graph.in_degree(weight="total_trade_value"),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    corridors = sorted(
        graph.edges(data=True),
        key=lambda x: x[2]["total_trade_value"],
        reverse=True
    )[:20]

    return {
        "generated_at": datetime.now(UTC).isoformat(),

        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),

        "density": nx.density(graph),

        "total_trade_value": total_trade,

        "top_exporters": exporters,

        "top_importers": importers,

        "top_trade_corridors": [
            {
                "source": u,
                "target": v,
                "trade_value": d["total_trade_value"]
            }
            for u, v, d in corridors
        ]
    }


def main():

    graph = load_trade_graph()

    stats = generate_statistics(graph)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            stats,
            f,
            indent=4
        )

    print("Saved:")
    print(OUTPUT)


if __name__ == "__main__":
    main()