"""
statistics.py

Generate summary statistics for cleaned UN Comtrade datasets.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, UTC

import pandas as pd


def generate_statistics(df: pd.DataFrame, dataset_name: str) -> dict:
    """
    Generate summary statistics for a cleaned trade dataframe.
    """

    trade_values = pd.to_numeric(
        df["trade_value_usd"],
        errors="coerce"
    ).fillna(0)

    stats = {
        "dataset": dataset_name,
        "generated_at": datetime.now(UTC).isoformat(),

        "trade_records": int(len(df)),

        "reporter_countries": int(df["reporterISO"].nunique()),
        "partner_countries": int(df["partnerISO"].nunique()),

        "unique_trade_pairs": int(
            df[["reporterISO", "partnerISO"]]
            .drop_duplicates()
            .shape[0]
        ),

        "exports": int(
            (df["flow"] == "Export").sum()
        ),

        "imports": int(
            (df["flow"] == "Import").sum()
        ),

        "total_trade_value": float(trade_values.sum()),
        "average_trade_value": float(trade_values.mean()),
        "median_trade_value": float(trade_values.median()),
        "min_trade_value": float(trade_values.min()),
        "max_trade_value": float(trade_values.max()),

        "missing_values": {
            col: int(df[col].isna().sum())
            for col in [
                "reporterISO",
                "partnerISO",
                "trade_value_usd"
            ]
        }
    }

    return stats


def save_statistics(
    stats: dict,
    output_directory: str | Path
) -> Path:
    """
    Save statistics.json.
    """

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = output_directory / "statistics.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            stats,
            f,
            indent=4
        )

    return output_path


if __name__ == "__main__":

    from pathlib import Path
    import sys

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(PROJECT_ROOT))

    from backend.data_pipeline.csv_loader import load_uncomtrade_csv
    from backend.data_pipeline.validators import validate_trade_dataframe
    from backend.data_pipeline.transformer import transform_trade_dataframe

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

    cleaned_df = transform_trade_dataframe(
        df,
        sector=dataset
    )

    stats = generate_statistics(
        cleaned_df,
        dataset
    )

    output_file = save_statistics(
        stats,
        output_dir
    )

    print("=" * 60)
    print("Statistics generated successfully.")
    print(output_file)
    print("=" * 60)