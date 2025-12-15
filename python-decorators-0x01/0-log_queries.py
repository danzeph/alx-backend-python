import sqlite3
import functools
import datetime



#### decorator to lof SQL queries
def log_queries(func):
 @functools.wraps(func)
 def wrapper(query, *args, **kwargs):
  start_time = datetime.datetime.now()
  result = func(query, *args, **kwargs)
  end_time = datetime.datetime.now()
  duration = (end_time - start_time).total_seconds()
  print(f"SQL {query} took {duration:.3f} seconds")
  return result
 return wrapper

 """ YOUR CODE GOES HERE"""

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
