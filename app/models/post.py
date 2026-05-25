from app.core.db_async import Base
from typing import Optional
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy.sql import func


if TYPE_CHECKING:
    from app.models.user import User

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str | None] = mapped_column(Text)
    image_filename: Mapped[Optional[str]] = mapped_column(nullable=True)
    likes: Mapped[int] = mapped_column(default=0)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    owner: Mapped["User"] = relationship("User", back_populates="posts")