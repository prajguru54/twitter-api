from .base import CRUDBase
from user_service.models import Tag
from user_service.schemas import TagSchema as TagCreateSchema
from sqlalchemy.orm import Session
from typing import List


class CRUDTag(CRUDBase[Tag, TagCreateSchema, TagCreateSchema]):
    def get_by_user_id(self, db: Session, user_id: int) -> List[Tag]:
        return db.query(Tag).filter(Tag.user_id == user_id).all()


crud_tag = CRUDTag(Tag)
