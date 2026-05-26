from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiosqlite

from pydantic import BaseModel



class ServerBD:
    def __init__(self):
        self.db_path = 'database/training.db'


    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS subcategorys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category_id INTEGER,
                    is_endled BOOL
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTs subsubcategorys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category_id INTEGER,
                    subcategory_id INTEGER
                )
            """)

            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    subcategory_id INTEGER,
                    subsubcategory_id INTEGER
                )
            """)

            await conn.commit()



class CategoryCreate(BaseModel):
    name: str


db = ServerBD()



@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.post('/add_category')
async def add_category(category: CategoryCreate):
    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute(
            "INSERT INTO categorys (name) VALUES (?)",
            (category.name,)
        )

        await conn.commit()

        return {"status": 'success', 'message': f'Category {category.name} successfull added!'}


@app.get('/get_categorys')
async def get_category():
    async with aiosqlite.connect(db.db_path) as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * from categorys")

        rows = await cursor.fetchall()

        return [{'id': r[0], 'name': r[1]} for r in rows]


@app.get('/get_subcategorys/{category_id}')
async def get_subcategory(category_id: int):
    async with aiosqlite.connect(db.db_path) as conn:
        cursor = await conn.cursor()
        await cursor.execute(
            "SELECT * from subcategorys where category_id = ?",
            (category_id,)
        )

        rows = await cursor.fetchall()

        return [
            {
                'id': r[0],
                'name': r[1],
                'category_id': r[2],
                'is_endled': r[3]
            } 
            for r in rows
        ]
