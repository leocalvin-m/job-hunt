import csv

def csv_to_md(csv_filepath, md_filepath):
    """Converts a CSV file to a markdown file."""
    with open(csv_filepath, 'r') as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # Assume the first row is the header
        
        # Calculate column widths
        column_widths = [len(header) for header in headers]
        for row in reader:
            for i, cell in enumerate(row):
                column_widths[i] = max(column_widths[i], len(cell))
        
        # Reset the CSV file pointer to the beginning
        csv_file.seek(0)
        reader = csv.reader(csv_file)
        
        with open(md_filepath, 'w') as md_file:
            # Write the header row
            md_file.write('| ' + ' | '.join(header.ljust(column_widths[i]) for i, header in enumerate(headers)) + ' |\n')
            
            # Write the separator row
            md_file.write('|' + '|'.join(':' + '-' * (width-1) for width in column_widths) + '|\n')
            
            # Write the data rows
            next(reader)  # Skip the header row
            for row in reader:
                md_file.write('| ' + ' | '.join(cell.ljust(column_widths[i]) for i, cell in enumerate(row)) + ' |\n')

if __name__ == "__main__":
    csv_filepath = './jobs.csv'  # Update this to your CSV file path
    md_filepath = './jobs.md'   # Update this to your desired MD file path
    csv_to_md(csv_filepath, md_filepath)
    print("Markdown file has been created successfully.")
