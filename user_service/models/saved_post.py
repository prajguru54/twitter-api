from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Column
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Mapped
from user_service.core.db.db_conf import Base
from .user import User

if TYPE_CHECKING:
    from . import Tag
    from . import PostTagAssociation


class SavedPost(Base):
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()

    # Relationship to user table
    user_id: int = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    saved_by: Mapped["User"] = relationship(
        "User", back_populates="saved_posts", uselist=False
    )

    tags: Mapped[List["Tag"]] = relationship(
        secondary="association_table", back_populates="posts"
    )

    child_associations: Mapped[List["PostTagAssociation"]] = relationship(
        back_populates="post"
    )
