import sqlite3


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        print("Connection made successfully via __enter__")
        self.conn.row_factory = sqlite3.Row
        return self.conn
        

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Connection closed via __exit__")


def main():
    with DatabaseConnection("users.db") as db:
        cur= db.execute("SELECT * FROM users")
        results = cur.fetchall()

        for row in results:
            print(dict(row))


if __name__ == "__main__":
    main()
