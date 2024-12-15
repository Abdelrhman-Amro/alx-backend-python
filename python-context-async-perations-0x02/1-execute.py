import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """
        Initialize the context manager with the database name, query, and parameters.
        :param db_name: Name of the database file.
        :param query: SQL query to be executed.
        :param params: Parameters for the query (optional).
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        """
        Open the database connection and execute the query.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params or ())
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Commit changes (if any) and close the database connection.
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Example Usage
if __name__ == "__main__":
    # Set up a test database
    db_name = "test.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 20)")
        cursor.execute("INSERT INTO users (name, age) VALUES ('Charlie', 40)")
        conn.commit()

    # Query the database using the custom context manager
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(db_name, query, param) as results:
        print("Query Results:")
        for row in results:
            print(row)
