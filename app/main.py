from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.api import pose

app = FastAPI(
    title="척추Ping API",
    version="1.0.0",
)

# CORS 설정 (dev or production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(pose.router, prefix="/api/pose", tags=["pose"])

@app.get("/")
async def root():
    return {"message": "백엔드 설정 통합 테스트"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

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

    return {"회원 수": count}
