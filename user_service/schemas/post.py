from typing import Optional

from pydantic import BaseModel, validator
from datetime import datetime


class PostSearchResponse(BaseModel):
    title: str
    description: Optional[str] = ""
    author: Optional[str] = ""
    date_posted: Optional[datetime] = None

    @validator(
        "date_posted",
        pre=True,
    )
    def convert_str_to_datetime(cls, v):
        converted_date = None
        if v and isinstance(v, str):
            try:
                converted_date = datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                try:
                    converted_date = datetime.strptime(v, "%Y-%m-%d")
                except Exception:
                    return converted_date

        return converted_date


# Shared properties
class PostSchema(PostSearchResponse):
    user_id: int


class PostSearch(BaseModel):
    keyword: str
    from_date: Optional[str] = "2023-12-20"
    sort_by: Optional[str] = "popularity"


class PostInDBBase(PostSchema):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class PostInDBResponse(PostInDBBase):
    pass
