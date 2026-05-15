import pandas as pd
import networkx as nx


TRADE_FILE = (
    "data/raw/trade/trade_edges.csv"
)


def load_trade_network():
    df = pd.read_csv(TRADE_FILE)

    G = nx.from_pandas_edgelist(
        df,
        source="source",
        target="target",
        edge_attr="weight",
        create_using=nx.DiGraph()
    )

    return G, df


if __name__ == "__main__":
    graph, df = load_trade_network()

    print(df.head())

    print(
        f"Nodes: {graph.number_of_nodes()}"
    )

    print(
        f"Edges: {graph.number_of_edges()}"
    )