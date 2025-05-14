from db import Base, engine
from models import Animal

#run only once to create table
Base.metadata.create_all(bind=engine)