# import asyncio
# import aiosqlite

# class DatabaseConnection:
#     def __init__(self, db: str):
#         self.db = db
#         self.conn = None

#     async def __aenter__(self):
#         self.conn = await aiosqlite.connect(self.db)
#         print("Connection made successfully via __aenter__")
#         return self.conn

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         if self.conn:
#             await self.conn.close()
#             print("Connection closed via __aexit__")


# async def main():
#     async with DatabaseConnection("users.db") as db:
#         db.row_factory = aiosqlite.Row

#         cur = await db.execute("SELECT * FROM users")
#         rows = await cur.fetchall()
        

#         for row in rows:
#             print(dict(row))


# if __name__ == "__main__":
#     asyncio.run(main())


import sqlite3


class DatabaseConnection:
    """Custom context manager for SQLite database connections"""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self
        print("Connection made successfully via __aenter__")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print("Connection closed via __aexit__")


def main():
    with DatabaseConnection("users.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        for row in results:
            print(dict(row))


if __name__ == "__main__":
    main()
    

