from pydantic import BaseModel


# Shared properties
class Tag(BaseModel):
    title: str
