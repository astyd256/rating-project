from sqlalchemy import create_engine

from .engine import get_engine
from .models import Base

def init_db(db_path: str) -> None:
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)