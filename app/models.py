from sqlalchemy import Column, Integer, String
from app.db import Base

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sound = Column(String, nullable=False)