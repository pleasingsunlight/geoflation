"""
event.py

Pydantic schema representing geopolitical events used throughout
Geoflation's simulation engine.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


# ============================================================
# Enumerations
# ============================================================

class EventType(str, Enum):
    sanction = "sanction"
    war = "war"
    tariff = "tariff"
    export_ban = "export_ban"
    import_ban = "import_ban"
    political_instability = "political_instability"
    natural_disaster = "natural_disaster"


class TradeSector(str, Enum):
    agriculture = "agriculture"
    automotive = "automotive"
    electronics = "electronics"
    energy = "energy"
    metals = "metals"


# ============================================================
# Event Schema
# ============================================================

class GeopoliticalEvent(BaseModel):
    """
    Standardized event representation.
    """

    event_type: EventType

    country: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO-3166 Alpha-3 country code"
    )

    sector: TradeSector

    severity: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Shock severity between 0 and 1."
    )

    @field_validator("country")
    @classmethod
    def normalize_country(cls, value: str) -> str:
        """
        Convert ISO codes to uppercase.
        """

        return value.upper()

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }


# ============================================================
# Local Testing
# ============================================================

if __name__ == "__main__":

    event = GeopoliticalEvent(
        event_type="sanction",
        country="rus",
        sector="energy",
        severity=0.85
    )

    print("=" * 60)
    print("Event validated successfully")
    print("=" * 60)
    print(event.model_dump())