# CSV Cleaner Pro

## Problem
Exported CSV files often have stray whitespace, empty rows, duplicate rows and rows with the wrong number of columns.

## Example output
Input (`examples/sample_input.csv`):

```text
 name , email ,country 
 Alice , alice@example.com , USA 
Bob,bob@example.com ,USA
Bob,bob@example.com,USA
   , , 
```

Output (`examples/sample_output.csv`), produced by running the script on the file above:

```text
name,email,country
Alice,alice@example.com,USA
Bob,bob@example.com,USA
```

## What it does
- Trims whitespace from header names and from every cell.
- Pads short rows with empty cells. Extra cells beyond the header are dropped only if they are empty.
- Rows whose extra cells contain data are not truncated: they are left out of the cleaned file and written to `rejected_rows.csv` (with their line number), and a warning reports how many.
- Removes rows where every cell is empty.
- Removes exact duplicate rows (compared after trimming), keeping the first occurrence.

## Quick start
Tested with Python 3.11. No external dependencies (standard library only).

```bash
pip install -r requirements.txt   # nothing to install, kept for consistency
python src/main.py
```

The cleaned file is written to `output/cleaned.csv` (git-ignored); rejected rows, if any, go to `output/rejected_rows.csv`. To use other files:

```bash
python src/main.py --input path/to/data.csv --output path/to/cleaned.csv
```

When there are rejected rows, `rejected_rows.csv` is written next to the `--output` file.

## Sample data
`examples/sample_input.csv` contains a small contact list with padded values, a duplicate and an empty row.
If the file is missing and no `--input` is given, the script recreates it before running.

## Adapting it to your data
Pass your own CSV with `--input`; the first row must be the header. Any column layout works.
Check `rejected_rows.csv` after each run: those rows usually come from unquoted commas inside a value.
