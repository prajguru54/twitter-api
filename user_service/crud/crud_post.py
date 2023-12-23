from .base import CRUDBase
from user_service.models import SavedPost
from user_service.schemas import PostSchema as PostCreateSchema
from sqlalchemy.orm import Session
from typing import List


class CRUDPost(CRUDBase[SavedPost, PostCreateSchema, PostCreateSchema]):
    def get_by_user_id(self, db: Session, user_id: int) -> List[SavedPost]:
        return db.query(SavedPost).filter(SavedPost.user_id == user_id).all()


crud_post = CRUDPost(SavedPost)
