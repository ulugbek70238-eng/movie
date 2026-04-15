import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from bot import send_notification
import crud, schemas
from crud import create_user_db, get_all_or_exact_user
from database import SessionLocal
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add_user")
async def add_user_api(name: str, phone_number: str):

    result = create_user_db(name=name, phone_number=phone_number)

    msg = f'<b>Новый пользователь</b> \n Имя: {name}, Номер телефона {phone_number}'
    send_notification(msg)

    return {"status": 1, "message": result}

@router.get("/get_all_or_exact_user")
async def get_users_api(uid: int = 0):
    result = get_all_or_exact_user(uid)
    if result:
        return {"status": 1, "message": result}
    return {"status": 0, "message": result}


@router.post("/movies", response_model=schemas.MovieResponse)
async def create_movie(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    image_url = None

    if file:
        path = f"{UPLOAD_DIR}/{file.filename}"
        with open(path, "wb") as f:
            f.write(file.file.read())
        image_url = path

    return crud.create_movie(db, title, description, image_url)


@router.get("/movies", response_model=list[schemas.MovieResponse])
async def get_all_movies(db: Session = Depends(get_db)):
    return crud.get_all_movies(db)


@router.get("/movies/top", response_model=list[schemas.MovieResponse])
async def top_movies(db: Session = Depends(get_db)):
    return crud.get_top_10_movies(db)


@router.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie_by_id(db, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie

@router.put("/movies/{movie_id}")
async def update_movie(
    movie_id: int,
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    return crud.update_movie(
        db,
        movie_id,
        schemas.MovieCreate(title=title, description=description)
    )


@router.post("/movies/{movie_id}/rate")
def rate_movie(
    movie_id: int,
    value: int = Form(...),
    db: Session = Depends(get_db)
):
    if value < 1 or value > 10:
        raise HTTPException(status_code=400, detail="Rating must be 1-10")

    movie = crud.add_rating(db, user_id=1, movie_id=movie_id, value=value)

    return {
        "message": "Rating added",
        "new_rating": movie.rating
    }

@router.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    return crud.delete_movie(db, movie_id)