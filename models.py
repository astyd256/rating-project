from sqlalchemy import Column, Integer, String, REAL, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    poster_url = Column(String, nullable=True)
    poster_blob = Column(LargeBinary, nullable=True)
    year = Column(Integer, nullable=True)
    imdb_rating = Column(Integer, nullable=True)
    imdb_votes = Column(Integer, nullable=True)
    tomatos_rating = Column(Integer, nullable=True)
    my_rating = Column(Integer, nullable=True)
    title_type = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    directors = Column(String, nullable=True)
    
#TODO: Add class Games and Companies
    