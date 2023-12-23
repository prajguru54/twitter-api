from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session

from .base import CRUDBase
from user_service.models import User
from user_service.schemas import UserCreate, UserUpdate
from user_service.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            name=obj_in.name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_password(update_function):
        def wrapper(*args, **kwargs):
            print(f"=======args: {args}")
            print(f"=======kwargs: {kwargs}")
            if len(args) > 1:
                if not isinstance(args[3], dict):
                    obj_in = args[3].model_dump(exclude_unset=True)
                else:
                    obj_in = args[3]
            if kwargs:
                if not isinstance(kwargs['obj_in'], dict):
                    obj_in = kwargs['obj_in'].model_dump(exclude_unset=True)
                else:
                    obj_in = kwargs['obj_in']

            # Check if 'password' key is present in the user input
            if "password" in obj_in:
                # Hash the password
                obj_in["hashed_password"] = get_password_hash(
                    obj_in["password"]
                )
            return update_function(*args, **kwargs)

        return wrapper

    @update_password
    def update(
        self,
        db: Session,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
        exclude_unset: bool = True,
        exclude_none: bool = False,
        exclude_defaults: bool = False,
    ) -> User:
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)


crud_user = CRUDUser(User)
