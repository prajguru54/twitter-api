from typing import List, TYPE_CHECKING


from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, Mapped
from user_service.core.db.db_conf import Base
from .user import User
from sqlalchemy import ForeignKey, Integer, Column

if TYPE_CHECKING:
    from . import SavedPost
    from . import PostTagAssociation


class Tag(Base):
    title: Mapped[str] = mapped_column()

    # Relationship to user table
    user_id: int = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    saved_by: Mapped["User"] = relationship(
        "User", back_populates="saved_tags", uselist=False
    )

    posts: Mapped[List["SavedPost"]] = relationship(
        secondary="association_table", back_populates="tags"
    )

    parent_associations: Mapped[List["PostTagAssociation"]] = relationship(
        back_populates="tag"
    )
