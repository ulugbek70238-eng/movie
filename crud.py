import models
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User
from database import get_db
import schemas


def get_all_or_exact_user(uid=0):
    db = next(get_db())
    print(db)
    if uid:
        exact_user = db.query(User).filter_by(id=uid).first()
        if exact_user:
            return exact_user
        return False
    all_users = db.query(User).all()
    return all_users


def create_user_db(name, phone_number):
    db = next(get_db())
    new_user = User(name=name, phone_number=phone_number)
    db.add(new_user)
    db.commit()
    return True


def get_all_movies(db: Session):
    return db.query(models.Movie).all()


def create_movie(db: Session, title: str, description: str, image_url=None):
    movie = models.Movie(
        title=title,
        description=description,
        image_url=image_url
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def add_rating(db: Session, user_id: int, movie_id: int, value: int):

    # ❗ ВСЕГДА СОЗДАЁМ НОВУЮ ОЦЕНКУ (не обновляем)
    new_rating = models.Rating(
        user_id=user_id,
        movie_id=movie_id,
        value=value
    )

    db.add(new_rating)
    db.commit()

    # 🔥 СЧИТАЕМ СРЕДНЕЕ ПО ВСЕМ ОЦЕНКАМ
    avg_rating = db.query(func.avg(models.Rating.value))\
        .filter(models.Rating.movie_id == movie_id)\
        .scalar()

    # обновляем фильм
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    movie.rating = round(avg_rating, 2)

    db.commit()
    db.refresh(movie)

    return movie


def get_top_10_movies(db: Session):
    return db.query(models.Movie)\
        .order_by(models.Movie.rating.desc())\
        .limit(10)\
        .all()

def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate):

    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        db_movie.title = movie.title
        db_movie.description = movie.description
        db.commit()
        db.refresh(db_movie)

    return db_movie

def delete_movie(db: Session, movie_id: int):

    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if db_movie:
        db.delete(db_movie)
        db.commit()

    return db_movie