import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Assuming the query is passed as a keyword argument or the first positional argument
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"Executing SQL query: {query}")
        else:
            print("No query provided.")
        # Call the original function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")