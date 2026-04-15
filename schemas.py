from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MovieCreate(BaseModel):
    title: str
    description: str

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    rating: float
    image_url: str | None

    class Config:
        from_attributes = True

class RatingCreate(BaseModel):
    value: int