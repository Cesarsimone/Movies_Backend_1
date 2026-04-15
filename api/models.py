# Configuration de mes classes python avec SQLAlchemy pour la gestion de la base de données
# Mes librairies

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship # permet de definir des relations de cle etrangeres entre les tables.
from database import Base

# Definition de nos Classes de modeles de données qui representent les tables de la base de donnéesasses
class Movie(Base):

    __tablename__="movies" # nom de la table dans la base de données
    movieId= Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    genres=Column(String)
    ratings=relationship("Rating", back_populates="movie", cascade="all, delete") # relation avec la table Rating, cascade pour supprimer les ratings associés si un film est supprimé
    links=relationship("Link", back_populates="movie", uselist=False, cascade="all, delete") 
    tags=relationship("Tag", back_populates="movie", cascade="all, delete") 


class Rating(Base):
    __tablename__= "ratings"

    userId=Column(Integer, primary_key=True, )
    movieId=Column(Integer, ForeignKey("movies.movieId"), primary_key=True) # cle etrangere vers la table movies
    rating=Column(Float, nullable=False)
    timestamp=Column(Integer)

    movie=relationship("Movie", back_populates="ratings") # relation inverse avec la table Movie

class Tag(Base):
    __tablename__="tags"

    userId=Column(Integer, primary_key=True)
    movieId=Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    tag=Column(String, primary_key=True)
    timestamp=Column(Integer)

    movie= relationship("Movie", back_populates="tags")

class Link(Base):
    __tablename__="links"

    movieId = Column(Integer, ForeignKey("movies.movieId"), primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(Integer)

    movie=relationship("Movie", back_populates="links")