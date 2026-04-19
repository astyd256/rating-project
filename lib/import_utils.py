import pandas as pd
import requests
import csv

from dotenv import load_dotenv
import os

import re
from typing import Optional, Tuple
from sqlalchemy.orm import class_mapper

from lib.db.session import get_session
from lib.db.models import Movie
from lib.db import crud


load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/" #TODO maybe remove this an all instances

INPUT_MD_FILE = "imdb_ratings.md"
OUTPUT_MD_FILE = "imdb_ratings_with_posters.md"

def parse_md_row(line: str, data_type: str) -> Optional[Tuple]:
    cols = [col.strip() for col in line.split('|')[1:-1]]
    if len(cols) < 9:
        return None
    
    # Take URL from tag <img>
    poster_match = re.search(r'src="([^"]+)"', cols[1])
    poster_url = poster_match.group(1) if poster_match else None
    
    # Clears rating from stars and other symbols
    imdb_rating_clean = re.sub(r'[^0-9.]', '', cols[3].split()[0]) if cols[3] else ''
    rating_clean = re.sub(r'[^0-9.]', '', cols[4].split()[0]) if cols[4] else ''
    if data_type == "movie":
        
        try:
            data = {
                "title": cols[0] or None,
                "poster_url": poster_url,
                "year": int(cols[2]) if cols[2] else None,
                "imdb_rating":  float(imdb_rating_clean) if imdb_rating_clean else None,
                "rating": float(rating_clean) if rating_clean else None,
                "title_type": cols[5] or None,
                "genres": cols[6] or None,
                "imdb_votes": int(cols[7]) if cols[7] else None,
                "directors": cols[8] or None,
            }
        except Exception:
            return None
        return data

def import_file(md_path: str, db_path: str, data_type: str, file_ext: str) -> int:

    inserted = 0
    with get_session(db_path) as session:
        if file_ext == "md":
            if data_type == "movie":
                with open(md_path, encoding="utf-8") as f:

                    # Skip header
                    next(f, None)
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('| --'):
                            continue
                        row = parse_md_row(line, "movie")
                        if not row:
                            continue
                        title = row.get("title")
                        if not title:
                            continue
                        _, entry_created = crud.upsert_movie(session, match_by_title=title, **row)
                        if entry_created:
                            inserted += 1
    return inserted