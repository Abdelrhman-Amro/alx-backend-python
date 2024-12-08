import time
import sqlite3
import functools

# Dictionary to store cached query results
query_cache = {}

# Decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection to the wrapped function
            result = func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after the function completes
            conn.close()
        return result
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the SQL query from arguments
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query is None:
            raise ValueError("A valid SQL query must be provided.")
        
        # Check if the query result is already cached
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
