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
- Pads short rows with empty cells and truncates long rows to the header length (extra columns are dropped).
- Removes rows where every cell is empty.
- Removes exact duplicate rows (compared after trimming), keeping the first occurrence.

## Quick start
Tested with Python 3.11. No external dependencies (standard library only).

```bash
pip install -r requirements.txt   # nothing to install, kept for consistency
python src/main.py
```

The cleaned file is written to `examples/sample_output.csv`.

## Sample data
`examples/sample_input.csv` contains a small contact list with padded values, a duplicate and an empty row.
If the file is missing, the script recreates it before running.

## Adapting it to your data
Replace `examples/sample_input.csv` with your own CSV (first row must be the header), or change `INPUT_PATH` and `OUTPUT_PATH` at the top of `src/main.py`.
Any column layout works; rows longer than the header lose their extra columns.
