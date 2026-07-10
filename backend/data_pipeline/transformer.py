"""
transformer.py

Transforms validated UN Comtrade data into Geoflation's
canonical trade dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
    "reporterISO",
    "reporter",
    "partnerISO",
    "partner",
    "sector",
    "commodity_code",
    "commodity",
    "trade_value_usd",
    "year",
    "flow",
]


COLUMN_MAPPING = {
    "reporterISO": "reporterISO",
    "reporterDesc": "reporter",
    "partnerISO": "partnerISO",
    "partnerDesc": "partner",
    "cmdCode": "commodity_code",
    "cmdDesc": "commodity",
    "primaryValue": "trade_value_usd",
    "refYear": "year",
    "flowDesc": "flow",
}


def transform_trade_dataframe(
    df: pd.DataFrame,
    sector: str,
) -> pd.DataFrame:
    """
    Convert a validated UN Comtrade dataframe into
    Geoflation's canonical trade dataset.
    """

    df = df.copy()

    # ----------------------------------------------------------
    # Keep only required columns
    # ----------------------------------------------------------

    df = df[list(COLUMN_MAPPING.keys())]

    # ----------------------------------------------------------
    # Rename columns
    # ----------------------------------------------------------

    df = df.rename(columns=COLUMN_MAPPING)

    # ----------------------------------------------------------
    # Add sector column
    # ----------------------------------------------------------

    df["sector"] = sector

    # ----------------------------------------------------------
    # Normalize string columns
    # ----------------------------------------------------------

    string_columns = [
        "reporterISO",
        "reporter",
        "partnerISO",
        "partner",
        "commodity",
        "flow",
    ]

    for col in string_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )

    # ----------------------------------------------------------
    # Convert numeric columns
    # ----------------------------------------------------------

    df["commodity_code"] = pd.to_numeric(
        df["commodity_code"],
        errors="coerce"
    )

    df["trade_value_usd"] = pd.to_numeric(
        df["trade_value_usd"],
        errors="coerce"
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    # ----------------------------------------------------------
    # Remove invalid rows
    # ----------------------------------------------------------

    df = df.dropna(
        subset=[
            "reporterISO",
            "partnerISO",
            "trade_value_usd",
            "commodity_code",
        ]
    )

    # ----------------------------------------------------------
    # Remove self-trade
    # ----------------------------------------------------------

    df = df[
        df["reporterISO"] != df["partnerISO"]
    ]

    # ----------------------------------------------------------
    # Remove zero-value trade
    # ----------------------------------------------------------

    df = df[
        df["trade_value_usd"] > 0
    ]

    # ----------------------------------------------------------
    # Sort
    # ----------------------------------------------------------

    df = df.sort_values(
        [
        "year",
        "reporterISO",
        "partnerISO",
        "commodity_code",
        ],
        ascending=[True, True, True, True],
    )

    df = df.reset_index(drop=True)

    # ----------------------------------------------------------
    # Reorder columns
    # ----------------------------------------------------------

    df = df[OUTPUT_COLUMNS]

    return df


def save_cleaned_dataframe(
    df: pd.DataFrame,
    output_directory: str | Path,
) -> Path:
    """
    Save cleaned dataframe.
    """

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = output_directory / "cleaned_trade.csv"

    df.to_csv(
        output_file,
        index=False,
    )

    return output_file


if __name__ == "__main__":

    import sys

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(PROJECT_ROOT))

    from backend.data_pipeline.csv_loader import (
        load_uncomtrade_csv,
    )

    from backend.data_pipeline.validators import (
        validate_trade_dataframe,
    )

    dataset = "energy"

    csv_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "trade"
        / "uncomtrade"
        / "raw"
        / f"{dataset}_trade.csv"
    )

    output_dir = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "trade"
        / "uncomtrade"
        / "processed"
        / dataset
    )

    df = load_uncomtrade_csv(csv_path)

    validate_trade_dataframe(df)

    clean_df = transform_trade_dataframe(
        df,
        sector=dataset,
    )

    output_file = save_cleaned_dataframe(
        clean_df,
        output_dir,
    )

    print("=" * 60)
    print("Transformation successful.")
    print(output_file)
    print("=" * 60)
    print(clean_df.head())
    print()
    print(clean_df.shape)