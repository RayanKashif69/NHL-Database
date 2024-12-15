import sys
sys.path.insert(0, "dependencies")  # Add the dependencies folder to the search path

import pymssql

# Database connection details
server = 'uranium.cs.umanitoba.ca'
database = 'cs3380'
username = ''
password = ''

try:
    # Connect to the database
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    
    # Execute the query
    query = "SELECT * FROM OfficialInfo"
    cursor.execute(query)
    
    # Fetch and print the results
    print("Results from OfficialInfo:")
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    cursor.close()
    conn.close()

except pymssql.Error as e:
    print("Error connecting to database:", e)
