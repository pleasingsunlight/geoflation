"""
trade_etl.py

End-to-end ETL pipeline for UN Comtrade datasets.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, UTC

from backend.data_pipeline.csv_loader import load_uncomtrade_csv
from backend.data_pipeline.validators import validate_trade_dataframe
from backend.data_pipeline.transformer import (
    transform_trade_dataframe,
    save_cleaned_dataframe,
)
from backend.data_pipeline.statistics import (
    generate_statistics,
    save_statistics,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "trade"
    / "uncomtrade"
    / "raw"
)

PROCESSED_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "trade"
    / "uncomtrade"
    / "processed"
)


def discover_datasets() -> list[tuple[str, Path]]:
    """
    Automatically discover *_trade.csv datasets.
    """

    datasets = []

    for csv_file in sorted(RAW_DATA_DIR.glob("*_trade.csv")):
        sector = csv_file.stem.replace("_trade", "")
        datasets.append((sector, csv_file))

    return datasets


def process_dataset(sector: str, csv_path: Path) -> dict:
    """
    Run the complete ETL pipeline for a single dataset.
    """

    print(f"\nProcessing {sector}...")

    df = load_uncomtrade_csv(csv_path)

    validate_trade_dataframe(df)

    cleaned_df = transform_trade_dataframe(
        df,
        sector=sector,
    )

    output_dir = PROCESSED_DATA_DIR / sector

    cleaned_path = save_cleaned_dataframe(
        cleaned_df,
        output_dir,
    )

    stats = generate_statistics(
        cleaned_df,
        sector,
    )

    stats_path = save_statistics(
        stats,
        output_dir,
    )

    print(f"  Cleaned data : {cleaned_path.name}")
    print(f"  Statistics   : {stats_path.name}")
    print(f"  Rows         : {len(cleaned_df):,}")

    return {
        "sector": sector,
        "rows": len(cleaned_df),
        "cleaned_path": cleaned_path,
        "statistics_path": stats_path,
    }


def main() -> None:

    print("=" * 70)
    print("Geoflation Trade ETL Pipeline")
    print("=" * 70)

    datasets = discover_datasets()

    if not datasets:
        raise FileNotFoundError(
            f"No *_trade.csv files found in:\n{RAW_DATA_DIR}"
        )

    summary = []

    for sector, csv_path in datasets:
        result = process_dataset(
            sector,
            csv_path,
        )
        summary.append(result)

    print("\n" + "=" * 70)
    print("ETL SUMMARY")
    print("=" * 70)

    total_rows = 0

    for result in summary:
        print(
            f"{result['sector']:<15}"
            f"{result['rows']:>10,} rows"
        )
        total_rows += result["rows"]

    print("-" * 70)
    print(f"Datasets processed : {len(summary)}")
    print(f"Total trade records: {total_rows:,}")
    print(
        f"Completed at       : "
        f"{datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()