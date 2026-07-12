"""
graph_exports.py

Exports useful graph metadata.
"""

from pathlib import Path
import json

import pandas as pd

from backend.graph.graph_loader import load_trade_graph


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "graph"
)


def export_neighbors(graph):

    neighbors = {}

    for node in graph.nodes():

        neighbors[node] = sorted(
            list(graph.successors(node))
        )

    with open(
        OUTPUT / "country_neighbors.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            neighbors,
            f,
            indent=4
        )


def export_sector_weights(graph):

    rows = []

    for u, v, d in graph.edges(data=True):

        for sector, value in d["sectors"].items():

            rows.append({

                "source": u,

                "target": v,

                "sector": sector,

                "trade_value": value

            })

    pd.DataFrame(rows).to_csv(

        OUTPUT / "sector_trade_weights.csv",

        index=False

    )


def export_top_corridors(graph):

    rows = sorted(

        graph.edges(data=True),

        key=lambda x: x[2]["total_trade_value"],

        reverse=True

    )

    rows = rows[:100]

    pd.DataFrame([

        {

            "source": u,

            "target": v,

            "trade_value": d["total_trade_value"]

        }

        for u, v, d in rows

    ]).to_csv(

        OUTPUT / "top_trade_corridors.csv",

        index=False

    )


def main():

    graph = load_trade_graph()

    export_neighbors(graph)

    export_sector_weights(graph)

    export_top_corridors(graph)

    print("=" * 60)
    print("Graph exports generated.")
    print("=" * 60)


if __name__ == "__main__":
    main()