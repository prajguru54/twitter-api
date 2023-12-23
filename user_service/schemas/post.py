from typing import Optional

from pydantic import BaseModel, validator
from datetime import datetime


# Shared properties
class PostSchema(BaseModel):
    title: str
    description: Optional[str] = ""
    author: Optional[str] = ""
    date_posted: Optional[str] = None
    user_id: int

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


class PostSearch(BaseModel):
    keyword: str
    from_date: Optional[str] = "2023-12-20"
    sort_by: Optional[str] = "popularity"
