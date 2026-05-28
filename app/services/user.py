from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate):

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user
    
    @staticmethod
    async def get_all_users(db: AsyncSession):

        result = await db.execute(select(User))
        return result.scalars().all()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str):
        result = await db.execute(
            select(User).where(
                User.username == username
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user(db: AsyncSession, db_user: User, updates: UserUpdate):
        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def delete_user(db: AsyncSession, db_user: User):

        await db.delete(db_user)
        await db.commit()