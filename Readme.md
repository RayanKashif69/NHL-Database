# Databases-Chogolisa


## Database Concepts and Design CG 47 - Ali - Rayan - Singh

### How to Populate the Database

 - `Ensure you are in the Populate directory of the project (Databases-Chogolisa/Populate).

1. **Ensure you have the necessary files:**
    - `create-table.sql`: Contains the SQL commands to create the necessary tables.
    - `ordered_inserts.sql`: Contains the sorted `INSERT` statements to populate the tables.
    - `drop.sql` : Contains the SQL commands to `DROP` the tables from the database
    - `populatescript.py`: Python script to drop and re-populate tables and data in small batches.
    - `auth.config ` : Contains the credentials for login to the sql server

2. **Configure the database connection:**
    - Edit the `auth.config` file with the database credentials (already set in the populate/auth.config):
     - username is nawaza1
     - password is 7951458
      ```
      [database]
      server = uranium.cs.umanitoba.ca
      database = cs3380
      username = your_username
      password = your_password
      ```


4. **Run the `populatescript.py` to drop existing tables, create tables and populate the database:**
    - Ensure you have Python installed
    - Run the `populatescript.py` script:
      ```
      python populatescript.py
      ```
      NOTE*** population wont run on aviary since there are no sql commands there.(discussed with Heather)



### How to Run the Interface
1. **Ensure you have the necessary files:**
    - `Ensure you are in the Interface directory of the project (Databases-Chogolisa/Interface).`

2. **Run the interface using the 'make' command**
    - Ensure you have Python installed. (this runs on aviary without any installations)

    - Run the following command:
      ```
      make run
      ```
    - Run `make help` to see help menu 

3. **Use the interface:**
    - Follow the on-screen instructions to navigate through the menu and execute queries.

