import asyncio
import aiosqlite

db_name = "../python-decorators-0x01/users.db"

async def async_fetch_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:", users)
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40:", older_users)
            return older_users

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    
asyncio.run(fetch_concurrently())
