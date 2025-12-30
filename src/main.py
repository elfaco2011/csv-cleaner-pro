from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent
EXAMPLES_DIR = HERE.parent / "examples"
INPUT_PATH = EXAMPLES_DIR / "sample_input.csv"
OUTPUT_PATH = EXAMPLES_DIR / "sample_output.csv"

logging.basicConfig(
    level=logging.INFO,
    format="[CSVCleanerPro] %(levelname)s - %(message)s",
)


def _ensure_demo_input() -> None:
    if INPUT_PATH.exists():
        return
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Creating demo input at %s", INPUT_PATH)
    with INPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([" name ", " email ", "country "])
        writer.writerow([" Alice ", " alice@example.com ", " USA "])
        writer.writerow(["Bob", "bob@example.com ", "USA"])
        writer.writerow(["Bob", "bob@example.com", "USA"])  # duplicate
        writer.writerow(["   ", " ", " "])  # empty row


def _read_rows() -> tuple[List[str], List[List[str]]]:
    with INPUT_PATH.open(newline="") as f:
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
    _ensure_demo_input()
    if not INPUT_PATH.exists():
        logging.error("Input file not found: %s", INPUT_PATH)
        return

    header, rows = _read_rows()
    if not header:
        logging.warning("Input appears empty, nothing to do.")
        return

    header = _clean_header(header)
    cleaned = _clean_rows(header, rows)

    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(cleaned)

    logging.info("Wrote cleaned CSV to %s (%d rows)", OUTPUT_PATH, len(cleaned))


if __name__ == "__main__":
    run()
