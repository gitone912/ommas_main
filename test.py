import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/pranaymishra/Desktop/sih1429/ommas_main/static/data/unsatisfactory_work_grade/nqm/indianqm.csv', sep='\t')

# Drop the 'State' column
print(df)
# df = df.drop(['State'])

# Convert the DataFrame to a list of dictionaries
json_data = df.to_dict(orient='records')

# Print the result
print(json_data)