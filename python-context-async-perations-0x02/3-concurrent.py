import asyncio
import aiosqlite

# Initialize the database with sample data
async def initialize_db(db_name):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Bob', 20)")
        await db.execute("INSERT INTO users (name, age) VALUES ('Charlie', 50)")
        await db.commit()

# Asynchronous function to fetch all users
async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            result = await cursor.fetchall()
            print("All Users:")
            for row in result:
                print(row)
            return result

# Asynchronous function to fetch users older than 40
async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            result = await cursor.fetchall()
            print("Users Older Than 40:")
            for row in result:
                print(row)
            return result

# Run the queries concurrently
async def fetch_concurrently():
    db_name = "test_async.db"
    await initialize_db(db_name)
    # Use asyncio.gather to run both functions concurrently
    await asyncio.gather(
        async_fetch_users(db_name),
        async_fetch_older_users(db_name)
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
