from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    @staticmethod
    async def create_post(db: AsyncSession, post_data: PostCreate, user_id: int, image_filename: str | None = None):
        new_post = Post(
            title=post_data.title,
            content=post_data.content,
            image_filename=image_filename,
            user_id=user_id
        )
        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)

        return new_post
    
    @staticmethod
    async def get_all_posts(db: AsyncSession):
        result = await db.execute(select(Post))

        return result.scalars().all()
    
    @staticmethod
    async def get_post_by_id(db: AsyncSession, post_id: int):
        result = await db.execute(select(Post).where(Post.id == post_id))

        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_posts_by_username(db: AsyncSession, username: str):
        result = await db.execute(select(Post).join(User).where(User.username == username))

        return result.scalars().all()
    
    @staticmethod
    async def like_post(db: AsyncSession, new_post: Post):
        new_post.likes += 1
        await db.commit()
        await db.refresh(new_post)

        return new_post
    
    @staticmethod
    async def update_post(db: AsyncSession, new_post: Post, updates: PostUpdate):

        update_data = updates.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(new_post, key, value)

        await db.commit()
        await db.refresh(new_post)

        return new_post
    
    @staticmethod
    async def delete_post(db: AsyncSession, new_post: Post):

        await db.delete(new_post)
        await db.commit()