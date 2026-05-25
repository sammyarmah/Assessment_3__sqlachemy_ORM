from app.core.db_async import Base
from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


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

    # Relationship
    owner: Mapped["User"] = relationship("User", back_populates="posts")