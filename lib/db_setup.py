import sqlite3

def init_db(db_path: str = "movies.db") -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        poster_url TEXT,
        year INTEGER,
        imdb_rating REAL,
        your_rating INTEGER,
        title_type TEXT,
        genres TEXT,
        num_votes INTEGER,
        directors TEXT
    )
    ''')
    conn.commit()
    conn.close()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base
# import requests

# DB_PATH = "sqlite:///data/movies.db"


# engine = create_engine(DB_PATH)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# def fetch_poster(title, url):
#     try:
#         response = requests.get(url, timeout=5)
#         if response.status_code == 200:
#             return response.content
#     except requests.RequestException:
#         pass
#     return None

# def add_movie(title, url):
#     poster_blob = fetch_poster(title, url)
#     movie = Movie(
#         title=title, 
#         poster_url=url, 
#         poster_blob=poster_blob)
#     session.add(movie)
#     session.commit()
    
# def get_poster(movie):
#     if movie.poster_url:
#         try:
#             response = requests.get(movie.poster_url, timeout=5)
#             if response.status_code == 200:
#                 return movie.poster_url
#         except requests.RequestException:
#             pass #If error - fallback to BLOB
#     return movie.poster_blob

    # add_movie("The Lord of The Rings", "https://m.media-amazon.com/images/M/MV5BMTZkMjBjNWMtZGI5OC00MGU0LTk4ZTItODg2NWM3NTVmNWQ4XkEyXkFqcGc@._V1_SX300.jpg")

    # movie = session.query(Movie).first()
    # poster = get_poster(movie)
    # print("using poster", poster if isinstance(poster, str) else "BLOB")