import sys
sys.path.insert(0, "dependencies")  # Add the dependencies folder to the search path

import pymssql
import configparser


def load_config():
    """Load database credentials from auth.config."""
    config = configparser.ConfigParser()
    config.read("populate/auth.config")
    return config["database"]


def connect_to_database():
    """Establish a connection to the database using credentials from auth.config."""
    config = load_config()
    try:
        connection = pymssql.connect(
            server=config["server"],
            user=config["username"],
            password=config["password"],
            database=config["database"]
        )
        print("Connected to the database successfully!")
        return connection
    except Exception as e:
        print("Failed to connect to the database. Error:", e)
        return None


def main_menu():
    """Display the main menu and handle navigation."""
    print("+---------------------------------------+")
    print("| NHL Query Interface                   |")
    print("+---------------------------------------+")
    print("| 1. Player Performance Queries         |")
    print("| 2. Team Dynamics Queries              |")
    print("| 3. Game Statistics Queries            |")
    print("| 4. Officiating Trends Queries         |")
    print("| 5. List All Teams                     |")
    print("| 6. Custom Query                       |")
    print("| 7. Exit                               |")
    print("+---------------------------------------+")
    choice = input("Enter your choice: ")
    return choice


def player_performance_menu():
    """Display the Player Performance Queries submenu."""
    while True:
        print("+---------------------------------------+")
        print("| Player Performance Queries            |")
        print("+---------------------------------------+")
        print("| 1. Top Scorers (Filter by Season)     |")
        print("| 2. Penalty Minutes (Filter by Team)   |")
        print("| 3. Most Game-Winning Goals            |")
        print("| 4. Player Trends Over Seasons         |")
        print("| 5. Top Performers by Birth City       |")
        print("| 6. Back to Main Menu                  |")
        print("+---------------------------------------+")
        
        choice = input("Enter your choice: ")

        if choice == '6':
            print("Returning to Main Menu...")
            break
        elif choice in ['1', '2', '3', '4', '5']:
            print(f"You selected option {choice}. Feature coming soon!")
        else:
            print("Invalid choice. Please select a valid option.")


def execute_query(connection, query, parameters=None):
    """Execute a SQL query and print the results."""
    try:
        cursor = connection.cursor(as_dict=True)
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print("Failed to execute query. Error:", e)


def list_all_teams(connection):
    """List all teams in the database."""
    query = "SELECT team_id, teamName FROM team_info;"
    try:
        cursor = connection.cursor(as_dict=True)
        cursor.execute(query)
        results = cursor.fetchall()
        print("+----------------+----------------+")
        print("| Team ID        | Team Name      |")
        print("+----------------+----------------+")
        for row in results:
            print(f"| {row['team_id']:<14} | {row['teamName']:<14} |")
        print("+----------------+----------------+")
    except Exception as e:
        print("Failed to execute query. Error:", e)


def handle_custom_query(connection):
    """Allow the user to run a custom query."""
    print("Enter your custom SQL query (type 'exit' to return to the main menu):")
    while True:
        query = input("SQL> ")
        if query.lower() == 'exit':
            break
        execute_query(connection, query)


def main():
    """Main function to handle the interface."""
    connection = connect_to_database()
    if not connection:
        return

    while True:
        choice = main_menu()
        if choice == '1':
            player_performance_menu()
        elif choice == '5':
            list_all_teams(connection)
        elif choice == '6':
            handle_custom_query(connection)
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Feature not implemented yet. Stay tuned!")

    connection.close()


if __name__ == "__main__":
    main()
