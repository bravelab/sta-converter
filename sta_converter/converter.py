import mt940
from pathlib import Path
import csv
import click

def convert_sta_to_csv(input_file, output_file):
    """
    Convert a single .sta file to CSV format.
    
    :param input_file: Path to the input .sta file
    :param output_file: Path to the output CSV file
    """
    # Parse the input STA/MT940 file using mt940.models.Transactions.from_file
    transactions = mt940.models.Transactions.from_file(input_file)

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Transaction Date', 'Entry Date', 'Amount', 'Currency', 'Transaction Type', 'Reference', 'Description']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for transaction in transactions:
            transaction_date = transaction.data.get('date', 'N/A')
            entry_date = transaction.data.get('entry_date', 'N/A')
            amount = transaction.data.get('amount', 'N/A')
            currency = transaction.data.get('currency', 'N/A')
            transaction_type = transaction.data.get('status', 'N/A')
            reference = transaction.data.get('transaction_reference', 'N/A')
            description = transaction.data.get('description', 'N/A')

            writer.writerow({
                'Transaction Date': transaction_date,
                'Entry Date': entry_date,
                'Amount': amount,
                'Currency': currency,
                'Transaction Type': transaction_type,
                'Reference': reference,
                'Description': description
            })


def process_directory(input_dir, output_dir):
    """
    Process all .sta files in the input directory and convert them to CSV files.
    
    :param input_dir: Directory containing .sta files
    :param output_dir: Directory to save the output CSV files
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for input_file in Path(input_dir).glob("*.sta"):
        output_file = Path(output_dir) / f"{input_file.stem}.csv"
        convert_sta_to_csv(input_file, output_file)


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def cli(input_dir, output_dir):
    """
    Command-line interface to process all .sta files in a directory and convert them to CSV.
    
    :param input_dir: Directory containing .sta files
    :param output_dir: Directory to save the output CSV files
    """
    print(f"Processing STA files from {input_dir} to {output_dir}...")
    process_directory(input_dir, output_dir)

if __name__ == '__main__':
    cli()