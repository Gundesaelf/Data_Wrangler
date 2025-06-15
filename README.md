# CSV Data Wrangler

This script is a command-line tool for exploring and cleaning CSV data files. It helps you inspect a dataset, remove duplicates, drop columns, handle missing values, normalize numeric data, and save a cleaned version — all through an interactive CLI.

## Features

- Searches your system for a specified CSV file (`C:/`, `D:/`, etc.)
- Displays basic dataset information
- Plots histograms for all columns
- Interactive prompts for:
  - Removing duplicate rows
  - Dropping specified columns
  - Handling missing data (drop, fill with 0, or fill with mode)
  - Normalizing numeric columns
- Saves the cleaned dataset with a new filename (prefixed with `wrangled_`)
- Colored terminal messages using `colorama` for better readability

## Installation

Install the required Python packages:

```bash
pip install pandas numpy matplotlib seaborn colorama
```

## Usage

Run the script from your terminal or command prompt:

```bash
python script_name.py
```

### Example Workflow

```
File Name: data.csv
Searching for 'data.csv'...
Found: D:\Documents\data.csv

DataFrame Info:
...

Do you want to drop duplicates? (y/n): y
Do you want to drop columns? (y/n): y
Enter columns to drop (comma-separated): id, timestamp
Do you want to handle missing data? (y/n): y
Normalize, drop, or fill?: fill
Fill with 0 or mode? mode
Do you want to save the file? (y/n): y
File saved as: wrangled_data.csv
```

## Notes

- Only `.csv` files are supported
- The file search is based on common Windows drive letters
- Histogram plots are generated using `matplotlib` and `seaborn`
- This tool is best suited for small to moderately sized datasets

## License

This script is provided as-is for personal or educational use. No license is applied by default.
