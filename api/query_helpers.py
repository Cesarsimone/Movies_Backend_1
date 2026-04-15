# Ce fichier nous permettra de recuperer les fonctions d'aides deja effectuer
# Import des librairies
from sqlalchemy.orm import Session
#from sqlalchemy import joinedload
from typing import Optional
import models

#............... Films............................
def get_movie(db: Session, movie_id:int):
    # on retourne un film par son Id
    return db.query(models.Movie).filter(models.Movie.movieId==movie_id).first()

def get_movies(db: Session, skip: int=0, limit: int =100, title: str= None, genre: str= None):
    # recupere une liste des films avec filtre optionnels
    query= db.query(models.Movie)

    if title:
        query=query.filter(models.Movie.title.ilike(f"%{title}%"))
    if genre:
        query=query.filter(models.Movie.genres.ilike(f"%{genre}%"))

    return query.offset(skip).limit(limit).all()


#................ Evaluations............................
def get_rating(db: Session, user_id:int, movie_id:int):
    # on recupere une evaluation en fonction du couple user_id et movie_id
    rating= db.query(models.Rating).filter(models.Rating.userId==user_id, models.Rating.movieId==movie_id).first()
    if rating is not None:
        return rating
    else:
        print("Aucune evaluation trouve pour ce couple user_id et movie_id.")
        return None

def get_ratings(db:Session, skip: int=0, limit: int=100, movie_id:int=None, user_id:int=None, min_Rating :float=None, max_Rating:float=None):
    # recupere une liste d'evaluation avec des filtres optionnels
    query= db.query(models.Rating)

    if movie_id:
        query=query.filter(models.Rating.movieId==movie_id)
    if user_id:
        query=query.filter(models.Rating.userId==user_id)   
    if min_Rating:
        query=query.filter(models.Rating.rating >= min_Rating)
    if max_Rating:
        query=query.filter(models.Rating.rating <= max_Rating)
    
    return query.offset(skip).limit(limit).all()


#.....................Tags............................
def get_tag(db:Session, user_id:int, movie_id:int, tag_text:str):
    # recupere un tag en fonction du couple user_id, movie_id et tag_text
    return db.query(models.Tag).filter(models.Tag.userId==user_id, models.Tag.movieId==movie_id, models.Tag.tag==tag_text).first()

def get_tags(db: Session, skip: int =0, limit: int=100, movie_id: Optional[int]=None, user_id: Optional[int]=None):
    #recupere une liste de tags avec des filtres optionnels
    query= db.query(models.Tag)
    if movie_id:
        query=query.filter(models.Tag.movieId==movie_id)    
    if user_id:
        query=query.filter(models.Tag.userId==user_id)
    return query.offset(skip).limit(limit).all()

#..................... Liens............................
def get_link(db: Session, movie_id:int):
    # recupere le lien Imdb et TMDb pour un film specifique associe
    return db.query(models.Link).filter(models.Link.movieId==movie_id).first()

def get_links(db: Session, skip: int=0, limit: int=100):
    # recupere une liste de liens avec des filtres optionnels
    return db.query(models.Link).offset(skip).limit(limit).all()

#.................Requetes analytiques.............................
def get_movie_count(db: Session):
    # recupere le nombre total de films
    return db.query(models.Movie).count()

def get_rating_count(db:Session):
    # recupere le nombre total d'evaluations
    return db.query(models.Rating).count()

def get_tag_count(db: Session):
    # recupere le nombre total de tags
    return db.query(models.Tag).count()

def get_link_count(db:Session):
    # recupere le nombre total de liens
    return db.query(models.Link).count()