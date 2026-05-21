from app.core.db import SessionLocal
from app.core.db_async import AsyncSessionLocal

# sync
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# async
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db