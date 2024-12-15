import os
import sqlite3
import pandas as pd

# Directory containing the CSV files (converted to WSL path format)
csv_directory = 'DataSet'

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('nhl.db')

# Function to create a table name from a file name
def create_table_name(file_name):
    return os.path.splitext(file_name)[0]

try:
    # Iterate over all CSV files in the directory
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(csv_directory, file_name)
            table_name = create_table_name(file_name)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Insert the DataFrame into the SQLite database
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f"Imported {file_name} into table {table_name}")

    # Commit the transaction
    conn.commit()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    conn.close()