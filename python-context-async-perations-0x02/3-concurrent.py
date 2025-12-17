import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users")
        result = await cur.fetchall()
        return result
    


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE age > ?",(40,))
        result = await cur.fetchall()
        return result
    

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users


def main():
    all_users, older_users  =asyncio.run(fetch_concurrently())
    # 3. Formatting the output to show dictionaries
    print("All Users:")
    for user in all_users:
        print(dict(user))  # Convert aiosqlite.Row to a standard dict

    print("\nUsers over 40:")
    for user in older_users:
        print(dict(user))    

if __name__ == "__main__":
    main()


