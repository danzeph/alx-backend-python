import time
import sqlite3 
import functools

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

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = kwargs.get('query') or (args[0] if args else None)
        if key in query_cache:
            print(f"fetching {key} using cached result")
            return query_cache[key]
        else:
             print(f"fetching {key} using {func.__name__}")
             result = func(*args, **kwargs)
             query_cache[key] = result
        return result
    return wrapper
    


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")


#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
