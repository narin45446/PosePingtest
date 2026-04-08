from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "google cloud run github actions 자동배포 테스트"}


@app.get("/health/db")
async def health_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {"database": "connected", "result": value}

@app.get("/health/members")
async def health_members():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM members"))
        count = result.scalar()

    return {"members_count": count}
