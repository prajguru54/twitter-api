from fastapi import APIRouter, Depends, Path
from user_service.schemas import (
    UserInDB,
    TagSchema,
    TagInDBResponse,
)
from sqlalchemy.orm import Session
from user_service.api import dependencies
from typing import List, Annotated
from user_service.crud import crud_tag, crud_post
from user_service.models import Tag
from user_service.core.errors import forbidden_exception
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


@router.post("/{post_id}", response_model=List[TagInDBResponse])
def create_tags(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
    post_id: Annotated[int, Path(title="Id of the post to tag", gt=0)],
    tags: List[TagSchema],
):
    post_to_tag = crud_post.get(db, post_id)
    tag_objs = [Tag(title=tag.title, saved_by=current_user) for tag in tags]
    for tag in tag_objs:
        tag.posts.append(post_to_tag)
    db.add_all(tag_objs)
    db.commit()
    return tag_objs


@router.put("/{post_id}", response_model=List[TagInDBResponse])
def update_tags(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
    post_id: Annotated[int, Path(title="Id of the post to tag", gt=0)],
    tags: List[TagSchema],
):
    post_to_tag = crud_post.get(db, post_id)
    tag_objs = [Tag(title=tag.title, saved_by=current_user) for tag in tags]
    if not tag_objs:
        return

    post_to_tag.tags = []
    for tag in tag_objs:
        tag.posts.append(post_to_tag)
    db.add_all(tag_objs)
    db.commit()
    return tag_objs


@router.get("/", response_model=list[TagInDBResponse])
def get_all_tags(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud_tag.get_by_user_id(db, user_id=current_user.id)


@router.get("/{post_id}", response_model=list[TagInDBResponse])
def get_all_tags_for_a_post(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
    post_id: Annotated[int, Path(title="Id of the post to tag", gt=0)]
):
    post_from_db = crud_post.get(db, post_id)
    if post_from_db.saved_by.id != current_user.id:
        raise forbidden_exception
    return post_from_db.tags
