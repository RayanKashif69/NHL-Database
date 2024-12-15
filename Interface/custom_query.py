from query_executor import execute_query

def handle_custom_query(connection):
    """Allow the user to run a custom query."""
    print("Enter your custom SQL query (type 'exit' to return to the main menu):")
    while True:
        query = input("SQL> ")
        if query.lower() == 'exit':
            break
        execute_query(connection, query)

