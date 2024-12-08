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

# Decorator to manage transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the wrapped function
            result = func(conn, *args, **kwargs)
            # Commit transaction if no errors
            conn.commit()
            return result
        except Exception as e:
            # Rollback transaction in case of error
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
