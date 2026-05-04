import networkx as nx


def build_trade_graph():
    G = nx.DiGraph()

    # Nodes
    countries = ["russia", "china", "eu", "usa", "middleeast"]

    for c in countries:
        G.add_node(c)

    # Edges (trade dependencies)
    edges = [
        ("russia", "eu", 0.9),
        ("russia", "china", 0.7),
        ("middleeast", "china", 0.8),
        ("china", "usa", 0.6),
        ("eu", "usa", 0.5),
    ]

    for src, tgt, w in edges:
        G.add_edge(src, tgt, weight=w)

    return G

def propagate_shock(event_country: str, severity: float):
    G = build_trade_graph()

    impacts = {}

    event_country = event_country.lower()

    if event_country not in G:
        return {}

    # Initial shock
    impacts[event_country] = severity

    # Spread shock
    for neighbor in G.successors(event_country):
        weight = G[event_country][neighbor]["weight"]
        impacts[neighbor] = round(severity * weight, 2)

    return impacts