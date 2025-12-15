import sqlite3
import functools
from datetime import datetime



#### decorator to lof SQL queries
def log_queries(func):
 @functools.wraps(func)
 def wrapper(*args, **kwargs):
  query = kwargs.get("query") if "query" in kwargs else args[0]
  start_time = datetime.now()
  result = func(query, *args, **kwargs)
  end_time = datetime.now()
  duration = (end_time - start_time).total_seconds()
  print(f"SQL {query} took {duration:.3f} seconds")
  return result
 return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
