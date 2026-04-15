# Usage de Pydantic pour definir le modele de donnees de mon API
# Import des librairies
from pydantic import BaseModel
from typing import Optional, List

#........ schemas de travail......
#Stuctures de donnnees definit pour la reception et l'envoi de donnees via l'API

class RatingBase(BaseModel):
    userId:int
    movieId:int
    rating:float
    timestamp:int

    class Config:
        orm_mode= True

class TagBase(BaseModel):
    userId:int
    movieId:int
    tag:str
    timestamp:int

    class Config:
        orm_mode= True

class MovieBase(BaseModel):
    movieId:int
    title:str
    genres:Optional[str]=None

    class Config:
        orm_mode= True

class MovieDetailed(MovieBase):
    ratings: List[RatingBase]= []
    tags:List[TagBase]= []
    link:Optional[LinkBase]=None

# Schemas pour liste de films (sans details imbrique)
class MovieSimple(BaseModel):
    movieId:int
    title:str
    genres:Optional[str]

    class Config:
        orm_mode= True


class LinkBase(BaseModel):
    imdbId:Optional[str]
    tmdbId:Optional[str]

    class Config:
        orm_mode= True

#... pour les endpoints de /ratings et tags 
class RatingSimple(BaseModel):
    userId:int
    movieId:int
    rating:float
    timestamp:int

    class Config:
        orm_mode= True

class TagSimple(BaseModel):
    userId:int
    movieId:int
    tag:str
    timestamp:int

    class Config:
        orm_mode= True

class LinkSimple(BaseModel):
    movieId:int
    imdbId:Optional[str]
    tmdbId: Optional[int] # ``Optional`` indique que ce champ peut être absent ou nul    
    class Config:
        orm_mode= True

class AnalyticsResponse(BaseModel):
    movie_count:int
    rating_count:int
    tag_count:int
    link_count:int