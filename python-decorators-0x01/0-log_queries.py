import sqlite3
import functools
from datetime import time

#### decorator to lof SQL queries
def log_queries(func):
 @functools.wraps(func)
 def wrapper(query, *args, **kwargs):
  start_time = time.time()
  functs = func(query, *args, **kwargs)
  endk_time = time.time()
  print(f"SQL {query} took {start_time -end_time}")
  return functs
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
