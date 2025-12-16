import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    conn = None
    def wrapper(*args, **kwargs):
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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction has been committed happy coding")
            return result
        except Exception as e:
            conn.rollback()
            print("Transaction rolled back")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=9, new_email='Crawford_Cartwright@hotmail.com')
