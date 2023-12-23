from fastapi import APIRouter, Depends
from user_service.schemas import PostSchema, PostSearch
from sqlalchemy.orm import Session
from user_service.api import dependencies
from typing import List
import requests
import os
from user_service.core import constants
from user_service.crud import crud_post
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()


@router.get("/", response_model=list[PostSchema])
def search_posts(
    *,
    db: Session = Depends(dependencies.get_db),
    posts_to_search: PostSearch,
):
    api_key = os.environ.get("API_KEY")
    url = (
        f"{constants.API_URL}?"
        f"q={posts_to_search.keyword}"
        f"&from={posts_to_search.from_date}"
        f"&sortBy={posts_to_search.sort_by}"
        f"&apiKey={api_key}"
    )

    response = requests.get(url)
    print(response.status_code)
    response_json = response.json()
    articles = response_json.get("articles")
    return [
        PostSchema(**article, date_posted=article["publishedAt"])
        for article in articles
    ]


@router.post("/")
def save_posts(
    *,
    db: Session = Depends(dependencies.get_db),
    posts_to_save: List[PostSchema],
):
    crud_post.create_many(db, posts_to_save)
