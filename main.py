from fastapi import FastAPI
from database import engine, Base
import models

from routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

# pip install fastapi uvicorn sqlalchemy python-multipart python-jose[cryptography] passlib[bcrypt]