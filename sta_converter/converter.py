from pathlib import Path
import csv
import click
from mt940 import MT940  # Assuming you saved the MT940 code as a module named 'mt940'

# Transaction type mapping
TRANSACTION_TYPE_MAPPING = {
    'S020': 'Cash deposit or direct credit',
    'S025': 'Bank transfer or electronic funds transfer (EFT)',
    'S034': 'Automated standing order payment',
    'S041': 'Salary payment or regular payments like pensions',
    'S073': 'Domestic or international payment (outward)',
    'S074': 'Internal transfer between accounts',
    'S075': 'Direct debit payment',
    'S076': 'SEPA credit transfer',
    'S087': 'Bank fee or service charge',
    'S094': 'Interest payment',
    'S096': 'Correction or adjustment transaction',
    'S940': 'MT940 statement generation or reconciliation entry'
}


def process_sta_files(input_dir, merged_output_file):
    """
    Process all .sta files in the input directory and merge their contents into a single CSV file.
    
    :param input_dir: Directory containing .sta files
    :param merged_output_file: Path to the final merged CSV file.
    """
    sta_files = list(Path(input_dir).glob("*.sta"))
    
    if not sta_files:
        print(f"No STA files found in {input_dir}")
        return

    # Open the merged CSV file for writing
    with open(merged_output_file, mode='w', newline='', encoding='utf-8') as merged_csv:
        # Define the base fieldnames (for common transaction information)
        fieldnames = ['Transaction Date', 'Booking Date', 'Amount', 'Currency', 'Transaction Type', 
                      'Transaction Type Description', 'Reference', 
                      'Description Part 1', 'Description Part 2', 'Description Part 3', 
                      'Description Part 4', 'Description Part 5', 'Description Part 6', 
                      'Description Part 7', 'Description Part 8', 'Description Part 9', 
                      'Description Part 10', 'Description Part 11', 'Description Part 12', 
                      'Description Part 13','Description Part 14']

        writer = csv.DictWriter(merged_csv, fieldnames=fieldnames)

        # Write header once (without description columns, which will be added dynamically)
        writer.writeheader()

        for sta_file in sta_files:
            mt940_parser = MT940(str(sta_file), encoding='latin-1')  # Specify 'latin-1' encoding

            print(f"Processing {sta_file}")

            for statement in mt940_parser.statements:
                transaction_count = 0  # Add a counter to see how many transactions are processed

                for transaction in statement.transactions:
                    transaction_count += 1
                    
                    # Lookup the transaction type description from the mapping dictionary
                    transaction_type = transaction.id
                    transaction_type_description = TRANSACTION_TYPE_MAPPING.get(transaction_type, 'Unknown')

                    # Split the description into parts based on semicolon (or another delimiter)
                    description_parts = transaction.description.split('\n')  # Adjust the delimiter if needed

                    # Dynamically generate the description column names
                    description_columns = {f'Description Part {i+1}': description_parts[i] 
                                           for i in range(len(description_parts))}
                    
        
                    
                    # Combine the base field values with the dynamic description parts
                    row_data = {
                        'Transaction Date': transaction.date,
                        'Booking Date': transaction.booking,
                        'Amount': transaction.amount,
                        'Currency': statement.start_balance.currency,
                        'Transaction Type': transaction_type,
                        'Transaction Type Description': transaction_type_description,  # Add the description
                        'Reference': transaction.reference,
                        **description_columns
                    }

                    # Dynamically update the CSV header if we encounter more description parts
                    # current_fieldnames = fieldnames + list(description_columns.keys())
                    # if set(writer.fieldnames) != set(current_fieldnames):
                    #     writer.fieldnames = current_fieldnames
                    #     merged_csv.seek(0)
                    #     # merged_csv.truncate()
                    #     writer.writeheader()

                    # Write the row data with dynamically created description columns
                    writer.writerow(row_data)

                # Debugging: Print how many transactions were processed for this statement
                print(f"Processed {transaction_count} transactions from {sta_file}")

    print(f"All STA files merged into {merged_output_file}")


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('merged_output_file', type=click.Path())
def cli(input_dir, merged_output_file):
    """
    Command-line interface to process all .sta files in a directory and merge them into a single CSV file.
    
    :param input_dir: Directory containing .sta files
    :param merged_output_file: Path to the final merged CSV file.
    """
    print(f"Processing STA files from {input_dir} and saving to {merged_output_file}...")
    process_sta_files(input_dir, merged_output_file)
    print(f"Merged CSV saved to {merged_output_file}")

if __name__ == '__main__':
    cli()