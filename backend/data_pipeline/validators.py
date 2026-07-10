"""
validators.py

Validation utilities for UN Comtrade datasets.

The validator checks that the dataset conforms to the expected
schema before downstream ETL processing.
"""

from __future__ import annotations

import pandas as pd


class ValidationError(Exception):
    """Raised when a dataset fails validation."""


# ---------------------------------------------------------------------
# Required columns
# ---------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "reporterISO",
    "reporterDesc",
    "partnerISO",
    "partnerDesc",
    "flowDesc",
    "cmdCode",
    "cmdDesc",
    "primaryValue",
]


VALID_FLOWS = {
    "Export",
    "Import",
}


# ---------------------------------------------------------------------
# Main validator
# ---------------------------------------------------------------------

def validate_trade_dataframe(df: pd.DataFrame) -> None:
    """
    Validate a UN Comtrade dataframe.

    Raises
    ------
    ValidationError
        If validation fails.
    """

    if df.empty:
        raise ValidationError("Dataset is empty.")

    _validate_required_columns(df)
    _validate_missing_values(df)
    _validate_trade_values(df)
    _validate_flow_types(df)
    _validate_cmd_code(df)


# ---------------------------------------------------------------------
# Individual validation functions
# ---------------------------------------------------------------------

def _validate_required_columns(df: pd.DataFrame) -> None:

    missing = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValidationError(
            "Missing required columns:\n"
            + "\n".join(missing)
        )


def _validate_missing_values(df: pd.DataFrame) -> None:

    critical = [
        "reporterISO",
        "partnerISO",
        "flowDesc",
        "primaryValue",
    ]

    for column in critical:

        if df[column].isna().any():

            count = int(df[column].isna().sum())

            raise ValidationError(
                f"{column} contains {count} missing values."
            )


def _validate_trade_values(df: pd.DataFrame) -> None:

    if not pd.api.types.is_numeric_dtype(df["primaryValue"]):
        raise ValidationError(
            "primaryValue must be numeric."
        )

    negatives = (df["primaryValue"] < 0).sum()

    if negatives > 0:
        raise ValidationError(
            f"Found {negatives} negative trade values."
        )


def _validate_flow_types(df: pd.DataFrame) -> None:

    flows = set(df["flowDesc"].dropna().unique())

    invalid = flows - VALID_FLOWS

    if invalid:
        raise ValidationError(
            f"Invalid flow types detected: {sorted(invalid)}"
        )


def _validate_cmd_code(df: pd.DataFrame) -> None:

    if df["cmdCode"].isna().any():

        raise ValidationError(
            "Commodity code contains missing values."
        )


# ---------------------------------------------------------------------
# Manual testing
# ---------------------------------------------------------------------

if __name__ == "__main__":

    from pathlib import Path
    import sys

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(PROJECT_ROOT))

    from backend.data_pipeline.csv_loader import load_uncomtrade_csv

    df = load_uncomtrade_csv(
        PROJECT_ROOT
        / "data"
        / "raw"
        / "trade"
        / "uncomtrade"
        / "raw"
        / "energy_trade.csv"
    )

    validate_trade_dataframe(df)

    print("=" * 60)
    print("Validation successful.")
    print("=" * 60)