from user_service.core.db.db_conf import Base

from sqlalchemy import Boolean, Column, String
from user_service.core.orm import TimestampMixin


class User(Base, TimestampMixin):
    name: str = Column(String, index=True, unique=True)
    email: str = Column(String, unique=True, index=True)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)
