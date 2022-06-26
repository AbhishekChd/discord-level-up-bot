import asyncio
import aiosqlite

async def test_example(loop):
    async with aiosqlite.connect('sqlite.db', loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 42;")
            r = await cur.fetchall()
            print(r)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_example(loop))