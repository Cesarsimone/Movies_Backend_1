# Travail avec SqlAlchemy pour la gestion de la base de données
#Configuration des librairies
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# chemin de la base de données
SQLALCHEMY_DATABASE_URL="sqlite:///./movies.db"
 
# Creation du moteur de base de donnees (engine) qui etablit la connexion a la base de donnees SQLITE (movies.db)
engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#definir la SessionLocal permettant de communiquer avec la BD
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Definir Base, qui servira de classe de base pour nosmodeles SQLAlchemy
Base=declarative_base()

#Testons notre script de connexion
#if __name__== "__main__":
#    try:
#        with engine.connect() as conn:
#            print("connexion reussie !")
#    except Exception as e:
#        print(f"Erreur de connection a la base de donnees: {e}")