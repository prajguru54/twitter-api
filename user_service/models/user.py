from user_service.core.db.db_conf import Base
from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, Column, String
from user_service.core.orm import TimestampMixin
from sqlalchemy.orm import relationship, Mapped


if TYPE_CHECKING:
    from . import SavedPost
    from . import Tag


class User(Base, TimestampMixin):
    name: str = Column(String, index=True, unique=True)
    email: str = Column(String, unique=True, index=True)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)

    saved_posts: Mapped[List["SavedPost"]] = relationship(
        "SavedPost",
        back_populates="saved_by",
        uselist=True,
        cascade="all,delete-orphan",
        passive_deletes=True,
    )
    saved_tags: Mapped[List["Tag"]] = relationship(
        "SavedPost",
        back_populates="saved_by",
        uselist=True,
        cascade="all,delete-orphan",
        passive_deletes=True,
    )
