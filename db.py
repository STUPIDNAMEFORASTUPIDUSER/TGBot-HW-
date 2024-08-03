import aiosqlite
from config import DB_NAME

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return result[0]
            else:
                return 0

async def get_user_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT score FROM users WHERE user_id = (?)', (user_id, )) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return result[0]
            else:
                return 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

async def update_user_score(user_id, new_score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT INTO users (user_id, score) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET score = excluded.score', (user_id, new_score))
        await db.commit()

async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER)''')
        await db.commit()
