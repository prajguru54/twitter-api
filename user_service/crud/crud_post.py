from .base import CRUDBase
from user_service.models import SavedPost
from user_service.schemas import PostSchema as PostCreateSchema


class CRUDPost(CRUDBase[SavedPost, PostCreateSchema, PostCreateSchema]):
    pass


crud_post = CRUDPost(SavedPost)
