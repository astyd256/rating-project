from sqlalchemy import create_engine
from typing import Dict

_engine_cache: Dict[str, object] = {}

def make_url(db_path: str) -> str:
    if db_path.startswith("sqlite:///") or "://" in db_path:
        return db_path
    return f"sqlite:///{db_path}"

def get_engine(db_path: str):
    url = make_url(db_path)
    if url not in _engine_cache:
        connect_args = {"check_same_thread": False} if url.startswith("sqlite:///") else {}
        _engine_cache[url] = create_engine(url, connect_args=connect_args, future=True)
    return _engine_cache[url]
