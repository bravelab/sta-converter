
# sta-converter

`sta-converter` is a command-line tool for converting `.sta` bank statement files (MT940 format) to CSV format and merging multiple CSVs into one for easier financial analysis and reporting.

## Features

- **Convert `.sta` files to CSV**: Extracts transaction data from `.sta` files into structured CSV files.
- **Batch Processing**: Automatically processes all `.sta` files in a given directory.
- **Merge CSVs**: Combines multiple CSV files into a single output file.

## Requirements

- Python 3.9+
- Dependencies managed by [Poetry](https://python-poetry.org/)

## Installation

1. Install Poetry if you haven't already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/bravelab/sta-converter.git
   cd sta-converter
   ```

3. Install the dependencies:

   ```bash
   poetry install
   ```

## Usage

Once installed, you can use the `sta-converter` CLI tool to convert `.sta` files to CSV and merge the results.

### Convert `.sta` Files to CSV

To convert `.sta` files into CSV files, use the following command:

```bash
poetry run sta_converter <input_dir> <output_dir> <merged_output_file>
```

### Example

```bash
poetry run sta_converter input output merged_output.csv
```

- **Install Dependencies**:

  ```bash
  poetry install
  ```

- **Run the CLI**:

  ```bash
  poetry run sta_converter <input_dir> <output_dir> <merged_output_file>
  ```

## License

This project is licensed under the MIT License.

## Author

Developed by Mariusz Smenżyk. You can reach out to me at mariusz@bravelab.io.
# sta-converter
