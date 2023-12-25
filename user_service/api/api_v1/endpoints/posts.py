from fastapi import APIRouter, Depends, Path
from user_service.schemas import (
    PostSchema,
    PostInDBResponse,
    PostSearchResponse,
    UserInDB,
)
from sqlalchemy.orm import Session
from user_service.api import dependencies
from typing import List, Annotated
import requests
import os
from user_service.core import constants
from user_service.crud import crud_post, crud_tag
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


@router.get("/search/{keyword}", response_model=list[PostSearchResponse])
def search_posts(
    *,
    db: Session = Depends(dependencies.get_db),
    keyword: Annotated[str, Path(title="keyword to search for")],
    from_date: str = "2023-12-23",
    sort_by: str = "popularity",
):
    api_key = os.environ.get("API_KEY")
    url = (
        f"{constants.API_URL}?"
        f"q={keyword}"
        f"&from={from_date}"
        f"&sortBy={sort_by}"
        f"&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response_json = response.json()
        print(f"Response Status Code - {response.status_code}")
        print(f"Response Headers - {response.headers}")
        print(f"Status - {response_json['status']}")
        print(f"totalResults - {response_json['totalResults']}")

        articles = response_json.get("articles")
        print(f"Article_1 - {articles[0]}")

        return [
            PostSearchResponse(**article, date_posted=article["publishedAt"])
            for article in articles
        ]
    except Exception as e:
        print(f"Some error occurred: {str(e)}")
        return []


@router.post("/", response_model=List[PostInDBResponse])
def save_posts(
    *,
    db: Session = Depends(dependencies.get_db),
    posts_to_save: List[PostSchema],
):
    return crud_post.create_many(db, posts_to_save)


@router.get("/", response_model=list[PostInDBResponse])
def get_all_posts(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
):
    return crud_post.get_by_user_id(db, user_id=current_user.id)


@router.get("/posts_by_tag/{tag}", response_model=list[PostInDBResponse])
def get_all_posts_with_a_specific_tag(
    *,
    current_user: Annotated[UserInDB, Depends(dependencies.get_current_user)],
    db: Session = Depends(dependencies.get_db),
    tag: Annotated[str, Path(title="tag title")],
):
    if tag_from_db := crud_tag.get_by_title(
        db, title=tag, user_id=current_user.id
    ):
        return tag_from_db.posts
    return []
