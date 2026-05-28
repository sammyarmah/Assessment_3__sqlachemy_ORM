from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.services.user import UserService
from app.schemas.user import UserRead, UserCreate

user_router = APIRouter()

@user_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await UserService.create_user(db, user_data)

@user_router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_async_db)):
    return await UserService.get_all_users(db)

@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):

    user = await UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK) 
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await UserService.delete_user(db, user)

    return {"message": "User deleted successfully"}

