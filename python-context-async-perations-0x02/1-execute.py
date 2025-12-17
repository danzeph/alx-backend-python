import sqlite3


class ExecuteQuery:
    def __init__(self, db: str):
        self.db = db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        print("Connection made successfully via __enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("Connection closed via __exit__")

    def execute_query(self, query, params=()):
        cur = self.conn.execute(query, params)
        results = cur.fetchall()

        for result in results:
            print(dict(result))


def main():
    with ExecuteQuery("users.db") as db:
        db.execute_query(
            "SELECT * FROM users WHERE age > ?",
            (25,)
        )


if __name__ == "__main__":
    main()
