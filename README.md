# CSV Cleaner PRO

General-purpose CSV cleaning utility that normalizes headers and rows, removes empty lines, and deduplicates records.

## What it does
- Reads `examples/sample_input.csv`.
- Trims whitespace from headers and cells.
- Normalizes row length (pads or truncates columns).
- Removes fully empty rows.
- Removes exact duplicate rows.
- Writes a cleaned dataset to `examples/sample_output.csv`.

## How to run (DEMO)
```bash
cd csv-cleaner-pro
python src/main.py
```

If `sample_input.csv` is missing, a small demo file is generated automatically.

## Inputs & outputs
- **Input:** `examples/sample_input.csv` (any messy CSV).
- **Output:** `examples/sample_output.csv` (cleaned, deduplicated CSV).

## Installation

```bash
pip install -r requirements.txt
```

## Project structure

- `src/` – core cleaning logic (entrypoint `src/main.py`).
- `examples/` – demo `sample_input.csv` and generated `sample_output.csv`.
- `docs/` – space for additional documentation or screenshots.

## Use cases

- Cleaning exported mailing lists or CRM exports before import.
- Normalizing messy spreadsheets from clients or team members.
- Preparing CSV datasets for analytics or BI tools.
