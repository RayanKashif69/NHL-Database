import configparser
import subprocess

def load_config():
    """Load database credentials from auth.config."""
    config = configparser.ConfigParser()
    config.read("\Project\auth.config")
    return config["database"]

subprocess.run(["sqlcmd", "-S", "uranium.cs.umanitoba.ca", "-d", "cs3380", "-U", "nawaza1", "-P", "7951458", "-i", "create-table.sql"], check=True)
def execute_sql_file(sql_file, server, database, username, password, batch_size=30000):
    """
    Execute a SQL file in batches using sqlcmd.

    :param sql_file: Path to the SQL file.
    :param server: MSSQL server address.
    :param database: Target database name.
    :param username: Username for MSSQL authentication.
    :param password: Password for MSSQL authentication.
    :param batch_size: Number of lines to execute per batch (default: 100).
    """
    try:
        # Read the SQL file content
        with open(sql_file, "r") as file:
            sql_content = file.readlines()

        # Split the SQL content into batches
        batch = []
        for i, line in enumerate(sql_content):
            batch.append(line)
            # If batch size is reached or it's the last line, execute the batch
            if (i + 1) % batch_size == 0 or i == len(sql_content) - 1:
                batch_sql = "".join(batch)
                execute_batch(batch_sql, server, database, username, password)
                batch = []  # Clear the batch after execution

        print("SQL file executed successfully.")
    except Exception as e:
        print(f"Error while executing the SQL file: {e}")


def execute_batch(batch_sql, server, database, username, password):
    """
    Execute a single batch of SQL commands using sqlcmd.

    :param batch_sql: SQL commands as a string.
    :param server: MSSQL server address.
    :param database: Target database name.
    :param username: Username for MSSQL authentication.
    :param password: Password for MSSQL authentication.
    """
    # Write the batch SQL to a temporary file
    temp_file = "temp_batch.sql"
    with open(temp_file, "w") as temp:
        temp.write(batch_sql)

    # Construct the sqlcmd command
    command = [
        "sqlcmd",
        "-S", server,
        "-d", database,
        "-U", username,
        "-P", password,
        "-i", temp_file
    ]

    # Execute the command
    subprocess.run(command, check=True)
    print("Batch executed successfully.")


# Load configuration
config = load_config()
sql_file = "sorted_nhl2.sql"  # Path to your sorted SQL file
server = config["server"]
database = config["database"]
username = config["username"]
password = config["password"]

# Run the script
execute_sql_file(sql_file, server, database, username, password)
