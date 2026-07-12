"""
event_mapper.py

Maps a validated geopolitical event onto the real
UN Comtrade trade graph.
"""

from __future__ import annotations

from backend.models.event import GeopoliticalEvent
from backend.ml_models.trade_propagation import propagate_trade_shock


def map_event_to_trade_network(
    event: GeopoliticalEvent,
    max_neighbors: int = 10,
) -> dict:
    """
    Convert a geopolitical event into
    affected trade partners.

    Returns
    -------
    dict
    """

    impacts = propagate_trade_shock(
        source_country=event.country,
        severity=event.severity,
        max_neighbors=max_neighbors,
    )

    return {
        "event_type": event.event_type,
        "country": event.country,
        "sector": event.sector,
        "severity": event.severity,
        "affected_countries": list(impacts.keys()),
        "shock_scores": impacts,
    }


if __name__ == "__main__":

    event = GeopoliticalEvent(
        event_type="sanction",
        country="RUS",
        sector="energy",
        severity=0.8,
    )

    result = map_event_to_trade_network(event)

    print()

    print("=" * 60)
    print("Mapped Event")
    print("=" * 60)

    from pprint import pprint

    pprint(result)