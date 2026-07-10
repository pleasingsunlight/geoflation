"""
csv_loader.py

Robust CSV loader for UN Comtrade exports.

Features
--------
- Handles malformed rows with trailing empty fields.
- Validates row length against header.
- Produces a clean pandas DataFrame.
"""

from pathlib import Path
import csv
import pandas as pd


class CSVLoaderError(Exception):
    """Raised when a CSV cannot be parsed correctly."""


def load_uncomtrade_csv(csv_path: str | Path) -> pd.DataFrame:
    """
    Load a UN Comtrade CSV while correcting malformed rows.

    Parameters
    ----------
    csv_path : str | Path
        Path to the raw CSV file.

    Returns
    -------
    pandas.DataFrame
    """

    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} does not exist.")

    with open(csv_path, "r", encoding="cp1252", newline="") as f:
        reader = csv.reader(f)

        try:
            header = next(reader)
        except StopIteration:
            raise CSVLoaderError("CSV file is empty.")

        expected_columns = len(header)

        records = []

        for line_number, row in enumerate(reader, start=2):

            # Remove trailing empty field produced by Comtrade export
            if len(row) == expected_columns + 1 and row[-1] == "":
                row = row[:-1]

            if len(row) != expected_columns:
                raise CSVLoaderError(
                    f"Malformed row detected.\n"
                    f"File: {csv_path.name}\n"
                    f"Line: {line_number}\n"
                    f"Expected {expected_columns} columns but found {len(row)}."
                )

            records.append(row)

    df = pd.DataFrame(records, columns=header)

    # ------------------------------------------------------------------
    # Normalize commonly used columns
    # ------------------------------------------------------------------

    numeric_columns = [
        "primaryValue",
        "cmdCode",
        "reporterCode",
        "partnerCode",
        "refYear"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    boolean_columns = [
        "isOriginalClassification",
        "isLeaf",
        "isReported"
    ]

    for col in boolean_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.lower()
                .map({
                    "true": True,
                    "false": False
                })
            )

    return df


if __name__ == "__main__":

    test_file = (
        Path("data")
        / "raw"
        / "trade"
        / "uncomtrade"
        / "raw"
        / "energy_trade.csv"
    )

    df = load_uncomtrade_csv(test_file)

    print("=" * 60)
    print("CSV loaded successfully")
    print("=" * 60)
    print(df.head())
    print()
    print("Shape:", df.shape)