from .models import Movie
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import class_mapper


def create_movie(session, **kwargs):
    """
    Create and persist a new Movie record.

    Parameters:
      session (Session): SQLAlchemy session used to add/flush the object.
      **kwargs: Movie fields (e.g., title='Inception', year=2010).

    Behavior:
      - Instantiates Movie(**kwargs) and adds it to the session.
      - Calls session.flush() to push pending changes and obtain DB-assigned values (like id)
        and to surface integrity errors early.
      - On IntegrityError, rolls back the session and re-raises the exception so callers
        can handle it.
      - Returns the Movie instance (attached to the session). Note: the instance may be
        in a partially flushed state until session.commit() is called.

    Raises:
      IntegrityError: if a DB constraint is violated during flush.
    """
    movie = Movie(**kwargs)
    session.add(movie)
    try:
        session.flush()  # to get id and catch errors
    except IntegrityError:
        session.rollback()
        raise
    return movie

def get_movie_by_title(session, title):
    """
    Retrieve a single Movie by title.

    Parameters:
      session (Session): SQLAlchemy session for querying.
      title (str): Movie title to match.

    Returns:
      Movie | None: The first Movie with a matching title, or None if not found.

    Notes:
      - Uses a simple equality filter. If titles are not unique, this returns the first match.
      - For case-insensitive matching, normalize title or use appropriate SQL functions.
    """
    return session.query(Movie).filter(Movie.title == title).first()

def upsert_movie(session, match_by_title, **kwargs):
    """
    Insert a new Movie or update an existing one by title.

    Parameters:
      session (Session): SQLAlchemy session used for querying and persisting.
      match_by_title (str): Title used to find an existing Movie.
      **kwargs: Fields to set on the Movie (used for both create and update).

    Returns:
      tuple(Movie, bool): (movie_instance, created)
        - movie_instance: the Movie object attached to the session.
        - created (bool): True if a new Movie was created, False if an existing one was updated.

    Behavior:
      - Attempts to find an existing Movie via get_movie_by_title().
      - If found, updates attributes from kwargs, re-adds the object to the session, and returns it with created=False.
      - If not found, constructs Movie(**kwargs), adds it to the session, and returns it with created=True.

    Notes:
      - This is a simple application-level upsert and is not atomic. Concurrent callers may
        create duplicates if run in parallel. For safe concurrency use a database-level upsert
        (e.g., INSERT ... ON CONFLICT / upsert APIs) or run inside a transaction with appropriate locks.
      - Callers should commit the session to persist changes.
    """
    allowed = {c.key for c in class_mapper(Movie).columns} - {"id"}
    # TODO: Check this T^2 algo latter
    good = {k: v for k, v in kwargs.items() if k in allowed}
    bad = [k for k in kwargs.keys() if k not in allowed]
    
    if bad:
        print(f"Skipped fields not in Movie model: {', '.join(bad)}")
    
    obj = get_movie_by_title(session, match_by_title)
    if obj:
        for k, v in good.items():
            setattr(obj, k, v)
        session.add(obj)
        return obj, False
    else:
        obj = Movie(**good)
        session.add(obj)
        return obj, True
