from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))