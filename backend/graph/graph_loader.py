"""
graph_loader.py

Loads the serialized UN Comtrade trade graph.
"""

from pathlib import Path
import pickle
import networkx as nx


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GRAPH_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "graph"
    / "trade_network.pkl"
)


def load_trade_graph() -> nx.DiGraph:

    if not GRAPH_FILE.exists():
        raise FileNotFoundError(
            f"Graph not found: {GRAPH_FILE}"
        )

    with open(GRAPH_FILE, "rb") as f:
        graph = pickle.load(f)

    return graph


if __name__ == "__main__":

    graph = load_trade_graph()

    print("=" * 60)
    print("Trade graph loaded successfully.")
    print(f"Nodes : {graph.number_of_nodes():,}")
    print(f"Edges : {graph.number_of_edges():,}")
    print("=" * 60)