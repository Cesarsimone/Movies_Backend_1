# Creation de notre Api
# Importation des librairies et modules necessaires
from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import query_helpers as helpers
import schemas


api_description= """ Bienvenue dans l'API de visualisation de données de MovieLens!"""

# Initialisation de l'application FastAPI
app= FastAPI(
    title="MovieLens API",
    description=api_description,
    version="1.0.0"
)

#Ecriture d'une fonction permettant d'ouvrir la session de base de donnnees
def get_db():
    db=SessionLocal() # ouverture de la session de base de données
    try:
        yield db #ici fastapi va gérer la fermeture de la session après l'utilisation
    finally:
        db.close()


#Routes ou endpoints pour tester la sante de l'api
@app.get("/",
         summary="Endpoint de test de santé de l'API",
         description="Cet endpoint permet de vérifier que l'API est opérationnelle ",
         response_description="Message de bienvenue confirmant que l'API est en ligne",
         operation_id="health_check",
         tags=["Santé de l'API"]
         )
async def health_check():
    return {"message": "Bienvenue dans l'API de visualisation de données de MovieLens!"}


#Routes ou endpoints pour obtenir un film par son ID
@app.get("/movies/{movie_id}",
  summary="Endpoint pour obtenir un film par son ID",
  description="Cet endpoint permet d'obtenir les détails d'un film en utilisant son ID unique",
  response_description="Details du film",
  response_model=schemas.MovieDetailed,
  tags=["films"],
  
)
def read_movie(movie_id: int = Path(..., description=" l'ID du film unique"), db:Session=Depends(get_db) ):
    movie=helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Film avec ID {movie_id} non trouvé !")
    return movie

# endpoint pour obtenir la liste des films avec pagination
@app.get("/movies",
         summary="Endpoint pour recuperer la liste des films avec pagination",
         description="Cet endpoint permet de recuperer la liste des films avec pagination",
         response_description="Liste des films avec pagination",
         response_model=List[schemas.MovieSimple],
         tags=["films"]
        )
def list_movies(skip: int= Query(0, ge=0, description="Nombre de resultats a ignorer"),
                limit: int= Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
                title: str=Query(None, description="Filtre par titre"),
                genre: str=Query(None, description="Filtre par genre"),
                db:Session=Depends(get_db)):
    movies=helpers.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return movies


#Endpoint pour obtenir une evaluation ou rating d'un film par utilsateur et film
@app.get("/ratings/{user_id}/{movie_id}", 
         summary="Endpoint pour obtenir une evaluation d'un film par utilisateur et film",
         description="Cet endpoint permet d'obtenir une evaluation d'un film en fonction de l'utilisateur et du film",
         response_description="Evaluation du film par l'utilisateur",
         response_model=schemas.RatingSimple,
         tags=["evaluations"]
        )
def read_rating(user_id: int = Path(..., description="ID de l'utilisateur"),
                movie_id: int=Path(..., description="ID du film"),
                db:Session=Depends(get_db)
    ):
        evaluation=helpers.get_rating(db, user_id=user_id,movie_id= movie_id)
        if evaluation is None:
            raise HTTPException(status_code=404, detail=f"Evaluation pour l'utilisateur {user_id} et le film {movie_id} non trouvée !") 
        return evaluation

# Endpoint pour obtenir une liste d'evaluations avec des filtres optionnels
@app.get( "/list_ratings", 
          summary="Endpoint pour obtenir une liste d'evaluations avec des filtres optionnels",
          description="Cet endpoint permet d'obtenir une liste d'evaluations en fonction de filtres optionnels comme l'ID du film, l'ID de l'utilisateur, la note minimale et maximale",
          response_description="Liste d'evaluations ",
          response_model=List[schemas.RatingSimple],
          tags=["evaluations"]
         )

def list_ratings(skip: int= Query(0, ge=0, description="Nombre de resultats a ignorer"),
                 limit: int= Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
                 movie_id: Optional[int]= Query(None, description="Filtre par ID de film"),
                 user_id: Optional[int]= Query(None, description="Filtre par ID d'utilisateur"),
                 min_Rating: Optional[float]= Query(None, ge=0, le=5, description="Filtre par note minimale"),
                 max_Rating: Optional[float]= Query(None, ge=0, le=5, description="Filtre par note maximale"),
                 db:Session=Depends(get_db)
    ):
        evaluations=helpers.get_ratings(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id, min_Rating=min_Rating, max_Rating=max_Rating)
        return evaluations

# Endpoint pour retourner un tag en fonction du couple user_id, movie_id et tag_text
@app.get("/tags/{user_id}/{movie_id}/{tag_text}",
         summary="Endpoint pour obtenir un tag en fonction du couple user_id, movie_id et tag_text",
         description="Cet endpoint permet d'obtenir un tag en fonction du couple user_id, movie_id et tag_text",
         response_description="Tag correspondant au couple utilisateur-film",
         response_model=schemas.TagSimple,
         tags=["tags"]
        )
def read_tag(user_id: int = Path(..., description="ID de l'utilisateur"),
             movie_id: int = Path(..., description="ID du film"),
             tag_text: str = Path(..., description="Texte du tag"),
             db: Session = Depends(get_db)):
    tag = helpers.get_tag(db, user_id=user_id, movie_id=movie_id, tag_text=tag_text)
    if tag is None:
        raise HTTPException(status_code=404, detail=f"Tag non trouvé pour l'utilisateur {user_id}, le film {movie_id} et le texte '{tag_text}'")
    return tag

# Endpoint pour obtenir une liste de tags avec des filtres optionnels
@app.get("/list_tags",  
         summary="Endpoint pour obtenir une liste de tags avec des filtres optionnels",
         description="Cet endpoint permet d'obtenir une liste de tags en fonction de filtres optionnels comme l'ID du film et l'ID de l'utilisateur",
         response_description="Liste de tags",
         response_model=List[schemas.TagSimple],
         tags=["tags"]
        )   
def list_tags(skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
              limit: int = Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
              movie_id: Optional[int] = Query(None, description="Filtre par ID de film"),
              user_id: Optional[int] = Query(None, description="Filtre par ID d'utilisateur"),
              db: Session = Depends(get_db)):   
    tags = helpers.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)
    return tags

# Endpoint pour obtenir les identifiants de liens (imdbId et tmdbId) pour un film donné
@app.get("/links/{movie_id}",   
         summary="Endpoint pour obtenir les identifiants de liens (imdbId et tmdbId) pour un film donné",
         description="Cet endpoint permet d'obtenir les identifiants de liens (imdbId et tmdbId) pour un film donné en fonction de son ID",
         response_description="Identifiants de liens pour le film",
         response_model=schemas.LinkSimple,
         tags=["liens"]
        )       
def read_link(movie_id: int = Path(..., description="ID du film"), db: Session = Depends(get_db)):
    link = helpers.get_link(db, movie_id=movie_id)
    if link is None:
        raise HTTPException(status_code=404, detail=f"Liens non trouvés pour le film avec ID {movie_id}")
    return link

#Endpoint pour retourner une liste pagines des idntifiants IMDB et TMDB pour les films
@app.get("/list_links",
         summary="Endpoint pour obtenir une liste paginée des identifiants IMDB et TMDB pour les films",
         description=" Cet endpoint permet d'obtenir une liste paginée des identifiants IMDB et TMDB pour les films, avec des filtres optionnels comme l'ID du film",
         response_description="Liste paginée des identifiants de liens pour les films",
         response_model=List[schemas.LinkSimple],
         tags=["liens"]
        )
def list_links(skip: int = Query(0, ge=0, description="Nombre de resultats a ignorer"),
               limit: int = Query(100, le=1000, description="Nombre maximal de resultats a retourner"),
               db: Session = Depends(get_db)):
     return helpers.get_links(db, skip=skip, limit=limit)

#Endpoint sur les statistiques ou analytics sur la base de données
@app.get("/analytics",
         summary="Endpoint pour obtenir des statistiques ou analytics sur la base de données",
         description="Retourne un resume analytique de la base de donnees:" \
         "- Nombre total de films" \
         "- Nombre total d'evaluations" \
         "- Nombre total de tags" \
         "- Nombre total de liens vers les bases de données externes (IMDB et TMDB)",
         response_description="Statistiques ou analytics sur la base de données",
         response_model=schemas.AnalyticsResponse,
         tags=["analytics"]
        )
def get_analytics(db: Session = Depends(get_db)):
    movie_count = helpers.get_movie_count(db)
    rating_count = helpers.get_rating_count(db)
    tag_count = helpers.get_tag_count(db)
    link_count = helpers.get_link_count(db)
    return schemas.AnalyticsResponse(movie_count=movie_count, rating_count=rating_count, tag_count=tag_count, link_count=link_count)