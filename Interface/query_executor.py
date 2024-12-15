

import sys
sys.path.insert(0, "dependencies")  # Add the dependencies folder to the search path


from prettytable import PrettyTable

def execute_query(connection, query, parameters=()):
    """Execute a parameterized SQL query and print the results."""
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query, parameters)
        results = cursor.fetchall()

        if not results:
            print("No data found.")
            return

        # Dynamically create a table with column names from query results
        table = PrettyTable()
        table.field_names = results[0].keys()  # Column names are the keys of the first row

        for row in results:
            table.add_row(row.values())  # Add row values to the table

        print(table)
    except Exception as e:
        print("Failed to execute query. Error:", e)
