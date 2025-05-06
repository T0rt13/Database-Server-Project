import mysql.connector
from mysql.connector import Error
import os

DB_CONFIG = {
  "host": os.environ['HOST'],
  "user": os.environ['USERNAME'],
  "password": os.environ["PASSWORD"]
}

DB_NAME = "reddit_clone_db"

### USE THESE 5 functions below to do basic crud operations on the mariadb

def create_connection(config):
    """Create a database connection to the MariaDB server."""
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f"Successfully connected to MariaDB server (version {connection.get_server_info()})")
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
    return connection

def create_database(connection, db_name):
    """Create a database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Database '{db_name}' ensured.")
        connection.database = db_name # Switch to the new database
    except Error as e:
        print(f"Error creating database '{db_name}': {e}")
    finally:
        cursor.close()

def execute_query(connection, query, params=None, multi=False):
    """Execute a single SQL query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or (), multi=multi)
        connection.commit()
        print("Query executed successfully.")
        return cursor # Return cursor for fetching results or lastrowid
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    # Not closing cursor here if we need to fetch results or get lastrowid

def fetch_all(cursor):
    """Fetch all rows from a cursor."""
    try:
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching results: {e}")
        return []
    finally:
        if cursor:
            cursor.close()

def fetch_one(cursor):
    """Fetch one row from a cursor."""
    try:
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching result: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def createDB():
    # 1. Establish initial connection (without specifying a database)
    cnx_server = create_connection(DB_CONFIG)

    if not cnx_server or not cnx_server.is_connected():
        print("Could not connect to MariaDB server. Exiting.")
        return

    # 2. Create the database if it doesn't exist
    create_database(cnx_server, DB_NAME)
    cnx_server.close() # Close server-level connection
    return

def createTable(db_name, sql_query):
    cnx_server = create_connection(DB_CONFIG)

    if not cnx_server or not cnx_server.is_connected():
        print("Could not connect to MariaDB server. Exiting.")
        return

    db_config_with_db = DB_CONFIG.copy()
    db_config_with_db["database"] = DB_NAME
    cnx = create_connection(db_config_with_db)

    if not cnx or not cnx.is_connected():
        print(f"Could not connect to database '{DB_NAME}'. Exiting.")
        return

    try:
        execute_query(cnx, sql_query)
    
    except Error as e:
        print(f"An error occurred during database operations: {e}")
    finally:
        if cnx and cnx.is_connected():
            cnx.close()
            print("\nMariaDB connection closed.")

