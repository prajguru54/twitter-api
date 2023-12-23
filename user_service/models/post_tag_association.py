from typing import TYPE_CHECKING


from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from user_service.core.db.db_conf import Base

if TYPE_CHECKING:
    from . import SavedPost
    from . import Tag


class PostTagAssociation(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("saved_post.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)
    # association between Assocation -> Child
    tag: Mapped["Tag"] = relationship(back_populates="parent_associations")

    # association between Assocation -> Parent
    post: Mapped["SavedPost"] = relationship(
        back_populates="child_associations"
    )
