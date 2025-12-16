import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            print("Connection has been established")

            result = func(conn, *args, **kwargs)
            return result

        finally:
            if conn:
                conn.close()
                print("Connection has been closed")
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)

                except sqlite3.OperationalError as e:
                    if "database is locked" not in str(e).lower():
                        raise

                    if attempt == retries:
                        print("Max retries reached")
                        raise

                    print(
                        f"Database locked "
                        f"(attempt {attempt}/{retries}) "
                        f"- retrying in {delay}s"
                    )
                    time.sleep(delay)
        return wrapper
    return decorator




@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
