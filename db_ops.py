import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

class MariaDB:
    def __init__(self):
        load_dotenv()
        self.config = {
            "host": "localhost",
            "port": 3306,
            "user": os.environ["MYSQL_USER"],
            "password": os.environ["MYSQL_PASSWORD"]
        }
        self.db_name = os.environ['MYSQL_DATABASE']
        self.create_database()
        self.create_tables()

    # ------------------------ Connect

    def create_connection(self, with_db=False):
        config = self.config.copy()
        if with_db:
            config["database"] = self.db_name
        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MariaDB: {e}")
        return None

    def create_database(self):
        conn = self.create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name} DEFAULT CHARACTER SET 'utf8mb4'")
                # print(f"Database '{self.db_name}' exists.")
            except Error as e:
                print(f"Error creating database '{self.db_name}': {e}")
            finally:
                cursor.close()
                conn.close()

    def execute_query(self, conn, query, params=None, fetch=False):
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            else:
                conn.commit()
                return True
        except Error as e:
            print(f"Error executing query: {e}\nQuery: {query}")
            return None
        finally:
            cursor.close()

    # ------------------------ Create tables

    def create_tables(self):
        self.create_database()
        conn = self.create_connection(with_db=True)
        if not conn:
            return

        create_posts_table = """
        CREATE TABLE IF NOT EXISTS posts (
            post_id VARCHAR(64) PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL,
            title TEXT NOT NULL,
            file_name TEXT NOT NULL,
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

        self.execute_query(conn, create_posts_table)
        self.execute_query(conn, create_upvotes_table)
        conn.close()
        # print("Tables created.")

    # ------------------------ CRUD operations

    def insert_post(self, conn, post_id, user_id, title, file_name):
        query = """
            INSERT INTO posts (post_id, user_id, title, file_name)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(conn, query, (post_id, user_id, title, file_name))

    def list_posts(self, conn):
        query = """
            SELECT 
                p.post_id,
                p.user_id,
                p.title,
                p.file_name,
                COUNT(u.user_id) AS upvote_count
            FROM posts p
            LEFT JOIN post_upvotes u ON p.post_id = u.post_id
            WHERE p.status = 'active'
            GROUP BY p.post_id, p.user_id, p.title, p.file_name
        """
        return self.execute_query(conn, query, fetch=True)

    def get_post(self, conn, post_id):
        query = """
            SELECT 
                p.post_id,
                p.user_id,
                p.title,
                p.file_name,
                COUNT(u.user_id) AS upvote_count
            FROM posts p
            LEFT JOIN post_upvotes u ON p.post_id = u.post_id
            WHERE p.status = 'active' AND p.post_id = %s
            GROUP BY p.post_id, p.user_id, p.title, p.file_name
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query, (post_id,))
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            else:
                return None
        finally:
            cursor.close()

    def update_post(self, conn, post_id, new_title, new_file_name):
        query = """
            UPDATE posts
            SET title = %s, file_name = %s
            WHERE post_id = %s AND status = 'active'
        """
        return self.execute_query(conn, query, (new_title, new_file_name, post_id))

    def soft_delete_post(self, conn, post_id):
        query = """
            UPDATE posts
            SET status = 'deleted'
            WHERE post_id = %s
        """
        return self.execute_query(conn, query, (post_id,))

    def upvote_post(self, conn, post_id, user_id):
        query = """
            INSERT INTO post_upvotes (post_id, user_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE post_id = post_id
        """
        return self.execute_query(conn, query, (post_id, user_id))

    def get_connection_with_db(self):
        return self.create_connection(with_db=True)


# ------------------------ Test
if __name__ == "__main__":
    db = MariaDB()
    db.create_tables()
    conn = db.get_connection_with_db()

    if conn:
        print("\n Inserting Post, database now has:")
        db.insert_post(conn, 'post4', 'user123', 'Hello World', 'pizza.jpg')
        print(db.list_posts(conn))

        print("\n Updating title, database now has:")
        db.update_post(conn, 'post4', 'Updated Title', 'taco.jpg')
        print(db.list_posts(conn))

        print("\n Upvoting Post, database now has:")
        db.upvote_post(conn, 'post4', 'user123')
        print(db.list_posts(conn))

        print("\n Deleting Post, database now has:")
        db.soft_delete_post(conn, 'post4')
        print(db.list_posts(conn))

        conn.close()
