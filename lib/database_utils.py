import sqlite3

DB_FILE = 'magazine.db'

def get_connection():
    """
    Establishes and returns a connection to the SQLite database with foreign key support enabled.
    The caller is responsible for closing the returned connection to avoid resource leaks.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_tables():
    """
    Creates the necessary database tables for the magazine application if they do not already exist.
    This function sets up the schema with proper foreign key relationships to maintain data integrity.
    It enables foreign key constraints and defines tables for authors, magazines, and articles.
    """
    # Establish a database connection with foreign key support
    conn = get_connection()
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Enable foreign key constraints for this connection (ensures referential integrity)
    cursor.execute("PRAGMA foreign_keys = ON;")
    # Create the authors table: stores author information with auto-incrementing ID and required name
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)
    # Create the magazines table: stores magazine information with auto-incrementing ID, required name and category
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
    """)
    # Create the articles table: stores article information with foreign keys linking to authors and magazines
    # Ensures that articles can only reference existing authors and magazines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        );
    """)
    # Commit all the table creation changes to the database
    conn.commit()
    # Close the database connection to free resources
    conn.close()
