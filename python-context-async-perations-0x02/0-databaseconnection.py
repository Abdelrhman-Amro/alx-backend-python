import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """Initialize with the database name."""
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """Open the database connection."""
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection."""
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Example usage
if __name__ == "__main__":
    # Set up a test database
    db_name = "test.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
        cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
        conn.commit()

    # Use the custom context manager to query the database
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)
