# Test de mon modeles de donnees definis
#Import des librairies
#%%
from database import SessionLocal, engine
from models import Base, Movie, Rating, Tag, Link


#Definition d'une session
db=SessionLocal()

#%%
#Tester la recuperation de quelques films
movies=db.query(Movie).limit(5).all()
for movie in movies:
    print(movie.movieId, movie.title, movie.genres)
else:
    print("Aucun film trouvé.")
# %%
# Recuperer les fimls du genre actions
action_movies=db.query(Movie).filter(Movie.genres.contains("Action")).limit(5).all()
for movie in action_movies:
    print(f"ID: {movie.movieId}, Title: {movie.title}, Genres: {movie.genres}")
# %%
#tester la Recupereration des evaluations.
ratings=db.query(Rating).limit(5).all()
for rating in ratings:
    print(f"UserID: {rating.userId}, MovieID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}")

# %%
# Recuperer les films avec la note suoerieur a 4
list_movies_sup_4=db.query(Movie.title, Rating.rating).join(Rating).filter(Rating.rating>=4).limit(5).all()
for title, rating in list_movies_sup_4:
    print(f"Title: {title}, Rating: {rating}"  )
# %%
# recuperation des tags axsocies aux films
tags=db.query(Tag).limit(5).all()
for tag in tags:
    print(f"UserID: {tag.userId}, MovieID: {tag.movieId}, Tag: {tag.tag}, Timestamp: {tag.timestamp}")
# %%
# tester la classe Link
links=db.query(Link).limit(5).all()
for link in links:  
    print(f"MovieID: {link.movieId}, ImdbID: {link.imdbId}, TMDbID: {link.tmdbId}")
# %%
#fermer la session
db.close()
# %%
