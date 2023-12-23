from typing import (
    Any,
    Dict,
    Generic,
    List,
    Type,
    TypeVar,
    Union,
    cast,
)
from user_service.core.errors import ResourceNotFoundException
from functools import cached_property
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from user_service.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, pk: Any) -> ModelType:
        if obj := (db.query(self.model).get(pk)):
            return cast(ModelType, obj)
        else:
            raise ResourceNotFoundException(pk=pk, type=self.model)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # sourcery skip: class-extract-method
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        try:
            return self._commit_and_refresh(db, db_obj)
        except Exception as e:
            print(f"Create unsuccessful: {str(e)}")
            db.rollback()
            raise e

    def create_many(
        self, db: Session, obj_ins: List[CreateSchemaType]
    ) -> None:
        db_objs = [self.model(**obj_in.model_dump()) for obj_in in obj_ins]
        try:
            db.add_all(db_objs)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise RuntimeError(e, self.model) from e

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[Dict[str, Any], UpdateSchemaType],
        exclude_unset: bool = True,
        exclude_none: bool = False,
        exclude_defaults: bool = False,
    ) -> ModelType:
        self._apply_properties(
            db_obj, obj_in, exclude_unset, exclude_none, exclude_defaults
        )
        db.add(db_obj)
        try:
            return self._commit_and_refresh(db, db_obj)
        except Exception as e:
            print(f"Update unsuccessful: {str(e)}")
            db.rollback()
            raise e

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj  # type:ignore

    def _commit_and_refresh(self, db: Session, obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(obj)
        return obj

    def _apply_properties(
        self,
        db_obj: ModelType,
        obj_in: Union[Dict[str, Any], UpdateSchemaType],
        exclude_unset: bool,
        exclude_none: bool,
        exclude_defaults: bool,
    ):
        mapper: Mapper = inspect(self.model)
        primary_key = set(self.primary_key_names)
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.model_dump(
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                exclude=primary_key,
            )
        )
        for column in mapper.attrs:
            if column.key in update_data:
                setattr(db_obj, column.key, update_data[column.key])

    @cached_property
    def primary_key_names(self) -> list[str]:
        mapper: Mapper = inspect(self.model)
        return [p.name for p in mapper.primary_key]
