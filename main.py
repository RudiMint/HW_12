from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import contacts
from src.routes import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.get("/")
def index():
    return {"message": "Contact App"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/api/test")
async def test(db: AsyncSession = Depends(get_db)):

    async with db.begin() as conn:
        row = await db.execute(text("SELECT current_database() AS database_name"))

    database_name = row.scalar() if row else None
    print(database_name)
    # try:
    #     # Make request
    #     result = await db.execute(text("SELECT * FROM users"))
    #     result = result.fetchone()
    #     if result is None:
    #         raise HTTPException(
    #             status_code=500, detail="Database is not configured correctly"
    #         )
    #     return {"message": "Welcome to FastAPI!"}
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=500, detail="Error connecting to the database")