from pathlib import Path
import csv
import click
from mt940 import MT940  # Assuming you saved the MT940 code as a module named 'mt940'


def convert_sta_to_csv(input_file, output_file):
    """
    Convert a single .sta file to CSV format.
    
    :param input_file: Path to the input .sta file
    :param output_file: Path to the output CSV file
    """
    mt940_parser = MT940(str(input_file), encoding='latin-1')  # Specify 'latin-1' encoding

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Transaction Date', 'Booking Date', 'Amount', 'Currency', 'Transaction Type', 'Reference', 'Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for statement in mt940_parser.statements:
            for transaction in statement.transactions:
                writer.writerow({
                    'Transaction Date': transaction.date,
                    'Booking Date': transaction.booking,
                    'Amount': transaction.amount,
                    'Currency': statement.start_balance.currency,
                    'Transaction Type': transaction.id,
                    'Reference': transaction.reference,
                    'Description': transaction.description
                })

def merge_csv_files(output_dir, merged_output_file):
    """
    Merge all CSV files in the output directory into a single CSV file.

    :param output_dir: Directory where individual CSV files are stored.
    :param merged_output_file: Path to the final merged CSV file.
    """
    csv_files = list(Path(output_dir).glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {output_dir}")
        return

    # Open the merged CSV file for writing
    with open(merged_output_file, mode='w', newline='', encoding='utf-8') as merged_csv:
        fieldnames = ['Transaction Date', 'Booking Date', 'Amount', 'Currency', 'Transaction Type', 'Reference', 'Description']
        writer = csv.DictWriter(merged_csv, fieldnames=fieldnames)

        # Write header only once
        writer.writeheader()

        for csv_file in csv_files:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as individual_csv:
                reader = csv.DictReader(individual_csv)
                # Write the rows from each individual CSV into the merged file
                for row in reader:
                    writer.writerow(row)

    print(f"All CSV files merged into {merged_output_file}")

def process_directory(input_dir, output_dir, merged_output_file):
    """
    Process all .sta files in the input directory, convert them to CSV files, 
    and merge all CSV files into a single CSV file.
    
    :param input_dir: Directory containing .sta files
    :param output_dir: Directory to save the individual CSV files
    :param merged_output_file: Path to the final merged CSV file
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Convert each STA file to a CSV file
    for input_file in Path(input_dir).glob("*.sta"):
        output_file = Path(output_dir) / f"{input_file.stem}.csv"
        convert_sta_to_csv(input_file, output_file)

    # Merge all the CSV files into one
    merge_csv_files(output_dir, merged_output_file)

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.argument('merged_output_file', type=click.Path())
def cli(input_dir, output_dir, merged_output_file):
    """
    Command-line interface to process all .sta files in a directory, convert them to CSV,
    and merge the CSVs into a single file.
    
    :param input_dir: Directory containing .sta files
    :param output_dir: Directory to save the individual CSV files
    :param merged_output_file: Path to the final merged CSV file
    """
    print(f"Processing STA files from {input_dir} and saving to {output_dir}...")
    process_directory(input_dir, output_dir, merged_output_file)
    print(f"Merged CSV saved to {merged_output_file}")

if __name__ == '__main__':
    cli()