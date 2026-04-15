#Ici nous allons tester nos fonctions d'aides ecrite
# Import des librairies
from database import SessionLocal
from query_helpers import *

# Definition d'une session
db=SessionLocal()

""" movies=get_movies(db, limit=5)
for movie in movies:
 print(movie.movieId, movie.title, movie.genres)
"""

""" rating= get_rating(db, user_id=1, movie_id=1)
if rating:
    print(f" MovieID: {rating.movieId}, Rating: {rating.rating}, Timestamp: {rating.timestamp}"   )"""

""" ratings=get_ratings(db, min_Rating=4, limit=5, user_id=5)
for rating in ratings:
    print(f" MovieID: {rating.movieId}, Rating: {rating.rating}"  )"""

n_movies =  get_movie_count(db)
print(f"Nombre total de films dans la base de données: {n_movies}")


db.close()   