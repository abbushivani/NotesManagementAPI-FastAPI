from fastapi import FastAPI

from app.database.database import Base, engine

from app.models.user import User
from app.models.note import Note
from app.routes.auth import router as auth_router
from app.routes.notes import router as notes_router


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
def home():
    return {"message": "Welcome to Notes Management API Running"}