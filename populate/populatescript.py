import sys
import pymssql
import configparser
import logging
import sys
import os

# Add the dependencies folder to the Python path
dependencies_path = "/mnt/d/Courses/COMP3380/PROJECT/Databases-Chogolisa/dependencies"
if os.path.isdir(dependencies_path):
    sys.path.insert(0, dependencies_path)
else:
    raise RuntimeError(f"Dependencies folder not found at: {dependencies_path}")



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def execute_sql_file(sql_file, connection, batch_size=30000):
    """
    Execute a SQL file in batches using pymssql.
    :param sql_file: Path to the SQL file.
    :param connection: pymssql connection object.
    :param batch_size: Number of lines to execute per batch (default: 30000).
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
                execute_batch(batch_sql, connection)
                batch = []  # Clear the batch after execution

        logging.info(f"{sql_file} executed successfully.")
    except FileNotFoundError:
        logging.error(f"SQL file not found: {sql_file}")
    except Exception as e:
        logging.error(f"Error while executing {sql_file}: {e}")

def execute_batch(batch_sql, connection):
    """
    Execute a single batch of SQL commands using pymssql.
    :param batch_sql: SQL commands as a string.
    :param connection: pymssql connection object.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(batch_sql)
            connection.commit()
            logging.info("Batch executed successfully.")
    except Exception as e:
        logging.error(f"Error while executing batch: {e}")
        connection.rollback()

def load_credentials(config_file):
    """
    Load database credentials from a config file.
    :param config_file: Path to the config file.
    :return: Dictionary containing server, database, username, and password.
    """
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        db_config = config["database"]
        return db_config["server"], db_config["database"], db_config["username"], db_config["password"]
    except KeyError as e:
        logging.error(f"Missing configuration key: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading configuration file: {e}")
        raise

if __name__ == "__main__":
    # Configuration
    config_file = "auth.config"

    # SQL file paths
    drop_sql_file = "drop.sql"
    create_table_sql_file = "create_table.sql"
    insert_sql_file = "ordered_inserts.sql"

    # Load credentials
    try:
        server, database, username, password = load_credentials(config_file)

        # Connect to the database
        with pymssql.connect(server, username, password, database) as connection:
            # Execute the scripts
            execute_sql_file(drop_sql_file, connection)
            execute_sql_file(create_table_sql_file, connection)
            execute_sql_file(insert_sql_file, connection)

    except Exception as e:
        logging.error(f"Script execution failed: {e}")
