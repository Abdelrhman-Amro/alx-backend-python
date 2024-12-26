import sqlite3
import functools

# Decorator to log SQL queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log the SQL query (assuming the query is passed as a keyword argument or positional argument)
            query = kwargs.get("query") or (args[0] if args else "Unknown Query")
            print(f"Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Set up a sample database for testing
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 20)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Charlie', 40)")
    conn.commit()
    conn.close()

# Setup the database and fetch users while logging the query
setup_database()
users = fetch_all_users(query="SELECT * FROM users")

print("\nFetched Users:")
for user in users:
    print(user)
