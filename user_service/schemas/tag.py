from pydantic import BaseModel
from typing import Optional


# Shared properties
class TagSchema(BaseModel):
    title: str


class TagInDBBase(TagSchema):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class TagInDBResponse(TagInDBBase):
    pass