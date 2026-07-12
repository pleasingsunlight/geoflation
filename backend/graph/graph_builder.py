"""
graph_builder.py

Builds the global directed trade graph from processed UN Comtrade datasets.
"""

from pathlib import Path
import pickle

import networkx as nx
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "trade"
    / "uncomtrade"
    / "processed"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "graph"
)

SECTORS = [
    "agriculture",
    "automotive",
    "electronics",
    "energy",
    "metals",
]


# ------------------------------------------------------------------
# ISO-3 validation
# ------------------------------------------------------------------

INVALID_CODES = {
    "W00",     # World
    "EUR",     # European Union
    "S19",     # Special Categories
    "899",     # Areas NES
    "_X",
    "X",
    "XX",
    "UNK",
    "",
}


def is_valid_country(code: str) -> bool:

    if pd.isna(code):
        return False

    code = str(code).strip().upper()

    if code in INVALID_CODES:
        return False

    return len(code) == 3 and code.isalpha()


# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "reporterISO",
    "partnerISO",
    "sector",
    "trade_value_usd",
]


def load_sector_dataframe(sector: str) -> pd.DataFrame:

    file_path = (
        PROCESSED_DATA
        / sector
        / "cleaned_trade.csv"
    )

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"{sector} missing columns: {missing}"
        )

    return df


# ------------------------------------------------------------------
# Graph construction
# ------------------------------------------------------------------

def build_trade_graph() -> nx.DiGraph:

    graph = nx.DiGraph()

    skipped_rows = 0

    for sector in SECTORS:

        print(f"Loading {sector}...")

        df = load_sector_dataframe(sector)

        # Remove aggregate / non-country entities
        df = df[
            df["reporterISO"].apply(is_valid_country)
            &
            df["partnerISO"].apply(is_valid_country)
        ]

        for _, row in df.iterrows():

            source = row["reporterISO"]
            target = row["partnerISO"]
            value = float(row["trade_value_usd"])

            if value <= 0:
                skipped_rows += 1
                continue

            if graph.has_edge(source, target):

                graph[source][target]["total_trade_value"] += value

                graph[source][target]["sectors"][sector] = (
                    graph[source][target]["sectors"].get(
                        sector,
                        0.0
                    )
                    + value
                )

            else:

                graph.add_edge(

                    source,

                    target,

                    total_trade_value=value,

                    sectors={
                        sector: value
                    }

                )

    print()
    print(f"Skipped zero-value rows : {skipped_rows:,}")

    return graph


# ------------------------------------------------------------------
# Save graph
# ------------------------------------------------------------------

def save_graph(graph: nx.DiGraph):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    graphml = OUTPUT_DIR / "trade_network.graphml"
    pickle_file = OUTPUT_DIR / "trade_network.pkl"

    # Save the full graph for the application
    with open(pickle_file, "wb") as f:
        pickle.dump(graph, f)

    # Build a visualization-friendly graph
    viz_graph = nx.DiGraph()

    for u, v, data in graph.edges(data=True):

        viz_graph.add_edge(
            u,
            v,
            total_trade_value=data["total_trade_value"]
        )

    nx.write_graphml(viz_graph, graphml)

    return graphml, pickle_file


# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

def print_summary(graph):

    total = sum(
        d["total_trade_value"]
        for _, _, d in graph.edges(data=True)
    )

    print("=" * 65)
    print("Trade Graph Summary")
    print("=" * 65)
    print(f"Nodes : {graph.number_of_nodes():,}")
    print(f"Edges : {graph.number_of_edges():,}")
    print(f"Total Trade Value : {total:,.2f}")
    print("=" * 65)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():

    print("=" * 65)
    print("Building Global Trade Graph")
    print("=" * 65)

    graph = build_trade_graph()

    graphml, pickle_file = save_graph(graph)

    print_summary(graph)

    print()
    print("Saved GraphML:")
    print(graphml)

    print()

    print("Saved Pickle:")
    print(pickle_file)


if __name__ == "__main__":
    main()