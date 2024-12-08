import time
import sqlite3
import functools

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

# Decorator to retry on transient failures
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    # Try executing the function
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    # Handle only specific transient errors (you can customize this)
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        # If out of retries, re-raise the exception
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users after retries: {e}")
