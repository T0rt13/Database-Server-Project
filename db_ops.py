import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": os.environ["MYSQL_USER"],
    "password": os.environ["MYSQL_PASSWORD"]
}
DB_NAME = os.environ['MYSQL_DATABASE']

# ------------------------ Connect

def create_connection(config):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MariaDB server")
            return connection
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
    return None

def create_database(connection, db_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"Database '{db_name}' ensured.")
    except Error as e:
        print(f"Error creating database '{db_name}': {e}")
    finally:
        cursor.close()

def execute_query(connection, query, params=None, fetch=False):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return True
    except Error as e:
        print(f"Error executing query: {e}\nQuery: {query}")
        return None
    finally:
        cursor.close()

# ------------------------ Create tables

def create_db_and_tables():
    conn = create_connection(DB_CONFIG)
    if not conn:
        return

    create_database(conn, DB_NAME)
    conn.close()

    db_config_with_db = DB_CONFIG.copy()
    db_config_with_db["database"] = DB_NAME
    conn = create_connection(db_config_with_db)
    if not conn:
        return

    create_posts_table = """
    CREATE TABLE IF NOT EXISTS posts (
        post_id VARCHAR(64) PRIMARY KEY,
        user_id VARCHAR(64) NOT NULL,
        title TEXT NOT NULL,
        content_key TEXT NOT NULL,
        status ENUM('active', 'deleted') DEFAULT 'active'
    )
    """

    create_upvotes_table = """
    CREATE TABLE IF NOT EXISTS post_upvotes (
        post_id VARCHAR(64),
        user_id VARCHAR(64),
        PRIMARY KEY (post_id, user_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
    )
    """

    execute_query(conn, create_posts_table)
    execute_query(conn, create_upvotes_table)
    conn.close()
    print("Tables created.")

# ------------------------ CRUD operations

def insert_post(conn, post_id, user_id, title, content_key):
    query = """
        INSERT INTO posts (post_id, user_id, title, content_key)
        VALUES (%s, %s, %s, %s)
    """
    return execute_query(conn, query, (post_id, user_id, title, content_key))

def list_posts(conn):
    query = """
        SELECT 
            p.post_id,
            p.user_id,
            p.title,
            p.content_key,
            COUNT(u.user_id) AS upvote_count
        FROM posts p
        LEFT JOIN post_upvotes u ON p.post_id = u.post_id
        WHERE p.status = 'active'
        GROUP BY p.post_id, p.user_id, p.title, p.content_key
    """
    return execute_query(conn, query, fetch=True)

def update_post(conn, post_id, new_title, new_content_key):
    query = """
        UPDATE posts
        SET title = %s, content_key = %s
        WHERE post_id = %s AND status = 'active'
    """
    return execute_query(conn, query, (new_title, new_content_key, post_id))

def soft_delete_post(conn, post_id):
    query = """
        UPDATE posts
        SET status = 'deleted'
        WHERE post_id = %s
    """
    return execute_query(conn, query, (post_id,))

def upvote_post(conn, post_id, user_id):
    query = """
        INSERT INTO post_upvotes (post_id, user_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE post_id = post_id
    """
    return execute_query(conn, query, (post_id, user_id))

# ------------------------ Get connection with DB
def get_db_connection():
    config_with_db = DB_CONFIG.copy()
    config_with_db["database"] = DB_NAME
    return create_connection(config_with_db)

# ------------------------ Test
if __name__ == "__main__":
    create_db_and_tables()
    conn = get_db_connection()

    if conn:
        print("\n Inserting Post, database now has:")
        insert_post(conn, 'post3', 'user123', 'Hello World', 'pizza.jpg')
        print(list_posts(conn))

        print("\n Updating title, database now has:")
        update_post(conn, 'post3', 'Updated Title', 'taco.jpg')
        print(list_posts(conn))

        print("\n Upvoting Post, database now has:")
        upvote_post(conn, 'post3', 'user123')
        print(list_posts(conn))

        print("\n Deleting Post, database now has:")
        soft_delete_post(conn, 'post3')
        print(list_posts(conn))

        conn.close()
