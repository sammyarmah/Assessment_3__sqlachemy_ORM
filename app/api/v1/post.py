from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.schemas.post import PostCreate, PostRead, PostUpdate
from app.services.post import PostService
from app.services.user import UserService
import shutil
from pathlib import Path


post_router = APIRouter()


@post_router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    username: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_async_db)
):
    user = await UserService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_filename = None
    if image:
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        image_path = upload_dir / image.filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_filename = image.filename
    
    post_data = PostCreate(title=title, content=content)

    return await PostService.create_post(db, post_data, owner_id=user.id, image_filename=image_filename)

@post_router.get("/", response_model=list[PostRead])
async def get_posts(db: AsyncSession = Depends(get_async_db)):
    return await PostService.get_all_posts(db)

@post_router.get("/{username}/posts", response_model=list[PostRead])
async def get_posts_by_user(
    username: str,
    db: AsyncSession = Depends(get_async_db)
):
    posts = await PostService.get_posts_by_username(db, username)
    return posts

@post_router.patch("/{post_id}", response_model=PostRead)
async def update_post(post_id:int, updates: PostUpdate, db: AsyncSession = Depends(get_async_db)):
    new_post = await PostService.get_post_by_id(db, post_id)

    if not new_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    updated_post = await PostService.update_post(db, new_post, updates)
    return updated_post

@post_router.post("/{post_id}/like", response_model=PostRead)
async def like_post(post_id:int, db:AsyncSession = Depends(get_async_db)):
    db_post = await PostService.get_post_by_id(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    liked_post = await PostService.like_post(db, db_post)
    return liked_post

@post_router.delete("/{post_id}", response_model=PostRead)
async def delete_post(post_id:int, db:AsyncSession = Depends(get_async_db)):
    db_post = await PostService.get_post_by_id(db, post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    await PostService.delete_post(db, db_post)
    return {"message": "Post deleted successfully"}