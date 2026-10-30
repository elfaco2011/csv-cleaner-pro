from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent
ROOT_DIR = HERE.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
DEFAULT_INPUT = EXAMPLES_DIR / "sample_input.csv"
DEFAULT_OUTPUT = ROOT_DIR / "output" / "cleaned.csv"

logging.basicConfig(
    level=logging.INFO,
    format="[CSVCleanerPro] %(levelname)s - %(message)s",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean a CSV file: trim, drop empty and duplicate rows.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help="input CSV (default: examples/sample_input.csv)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="cleaned CSV (default: output/cleaned.csv)")
    return parser.parse_args()


def _ensure_demo_input() -> None:
    if DEFAULT_INPUT.exists():
        return
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Creating demo input at %s", DEFAULT_INPUT)
    with DEFAULT_INPUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([" name ", " email ", "country "])
        writer.writerow([" Alice ", " alice@example.com ", " USA "])
        writer.writerow(["Bob", "bob@example.com ", "USA"])
        writer.writerow(["Bob", "bob@example.com", "USA"])  # duplicate
        writer.writerow(["   ", " ", " "])  # empty row


def _read_rows(input_path: Path) -> tuple[List[str], List[List[str]]]:
    with input_path.open(newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return [], []
        rows = [row for row in reader]
    return header, rows


def _clean_header(header: List[str]) -> List[str]:
    return [col.strip() for col in header]


def _normalize_row(row: List[str], size: int) -> List[str]:
    row = [cell.strip() for cell in row]
    if len(row) < size:
        row = row + ["" for _ in range(size - len(row))]
    elif len(row) > size:
        row = row[:size]
    return row


def _is_empty(row: List[str]) -> bool:
    return all(cell == "" for cell in row)


def _clean_rows(header: List[str], rows: List[List[str]]) -> List[List[str]]:
    cleaned: List[List[str]] = []
    seen: set[tuple[str, ...]] = set()
    size = len(header)
    for raw in rows:
        row = _normalize_row(raw, size)
        if _is_empty(row):
            continue
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(row)
    return cleaned


def run() -> None:
    args = _parse_args()
    if args.input == DEFAULT_INPUT:
        _ensure_demo_input()
    if not args.input.exists():
        logging.error("Input file not found: %s", args.input)
        sys.exit(1)

    header, rows = _read_rows(args.input)
    if not header:
        logging.warning("Input appears empty, nothing to do.")
        return

    header = _clean_header(header)
    cleaned = _clean_rows(header, rows)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(cleaned)

    logging.info("Wrote cleaned CSV to %s (%d rows)", args.output, len(cleaned))


if __name__ == "__main__":
    run()
