import csv
from itertools import islice
import pandas as pd

def preprocess_csv(input_file_path, output_file_path):
    print(f"Preprocessing {input_file_path}")
    print(f"Saving preprocessed data to {output_file_path}")
    try:
        # Read the CSV file and skip the first two rows
        with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Skip the first two rows
            rows_to_skip = 2
            reader = islice(reader, rows_to_skip, None)

            # Write the remaining rows to the output file
            for row in reader:
                writer.writerow(row)

        print(f"First two rows deleted from {input_file_path}. Result saved to {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Read the preprocessed CSV into a DataFrame
    df = pd.read_csv(output_file_path)

    # Select the columns to keep
    columns_to_keep = ['Textbox18', 'Textbox33', 'LOCATION_NAME', 'IMS_YEAR', 'Textbox8', 'TOTAL_PROPOSALS',
                       'LEN_COMPLETED', 'EXP_AMT', 'Textbox4', 'Textbox14', 'Textbox19', 'Textbox37', 'Textbox43']

    df = df[columns_to_keep]

    # Rename the columns with relevant names
    new_column_names = {
        'Textbox18': 'State',
        'Textbox33': 'IMS_Year_Category',
        'LOCATION_NAME': 'Location',
        'IMS_YEAR': 'Description',
        'Textbox8': 'Total_Inspection_Completed_Works',
        'TOTAL_PROPOSALS': 'Completed_Works_U%',
        'LEN_COMPLETED': 'Ongoing_Works',
        'EXP_AMT': 'Ongoing_U%',
        'Textbox4': 'Maintenance_Works',
        'Textbox14': 'Maintenance_U%',
        'Textbox19': 'Bridge_Works',
        'Textbox37': 'Bridge_U%',
        'Textbox43': 'Total_Inspection'
    }

    df.rename(columns=new_column_names, inplace=True)

    # Drop the 'State' column
    df = df.drop(['State'], axis=1)

    # Save the final DataFrame to the output file
    df.to_csv(output_file_path, index=False)

    return output_file_path

# Example usage:
# input_file_path = '/Users/pranaymishra/Desktop/sih1429/ommas_main/static/data/unsatisfactory_work_grade/nqm/rawnqm.csv'
# output_file_path = '/Users/pranaymishra/Desktop/sih1429/ommas_main/static/data/unsatisfactory_work_grade/nqm/prorawnqm.csv'

# preprocessed_file_path = preprocess_csv(input_file_path, output_file_path)
# print(f"Preprocessed data saved to: {preprocessed_file_path}")
