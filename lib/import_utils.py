import pandas as pd
import requests
import csv

from dotenv import load_dotenv
import os

import sqlite3
import re
from pathlib import Path
from typing import Optional, Tuple

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/" #TODO maybe remove this an all instances

INPUT_MD_FILE = "imdb_ratings.md"
OUTPUT_MD_FILE = "imdb_ratings_with_posters.md"

def parse_md_row(line: str) -> Optional[Tuple]:
    cols = [col.strip() for col in line.split('|')[1:-1]]
    if len(cols) < 9:
        return None
    
    # Достаем URL из тега <img>
    poster_match = re.search(r'src="([^"]+)"', cols[1])
    poster_url = poster_match.group(1) if poster_match else None
    
    # Очищаем рейтинги от звезд и других символов
    imdb_rating_clean = re.sub(r'[^0-9.]', '', cols[3].split()[0]) if cols[3] else ''
    your_rating_clean = re.sub(r'[^0-9.]', '', cols[4].split()[0]) if cols[4] else ''
    
    try:
        data = (
            cols[0],
            poster_url,
            int(cols[2]) if cols[2] else None,
            float(imdb_rating_clean) if imdb_rating_clean else None,
            int(float(your_rating_clean)) if your_rating_clean else None,
            cols[5],
            cols[6],
            int(cols[7].replace(',', '')) if cols[7].replace(',', '').isdigit() else 0,
            cols[8]
        )
    except (ValueError, IndexError):
        return None
    return data

def import_from_md(md_path: str, db_path: str) -> int:
    p = Path(md_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {md_path}")
    inserted = 0
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with p.open('r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines[2:]:
        line = line.strip()
        if not line or line.startswith('| --'):
            continue
        row = parse_md_row(line)
        if not row:
            continue
        cursor.execute('''
            INSERT INTO movies (title, poster_url, year, imdb_rating, your_rating, title_type, genres, num_votes, directors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)
        inserted += 1
    conn.commit()
    conn.close()
    return inserted

#---------------------------------------------------------
# Unredacted tools
# TODO: Rewrote these:

def imdb_csv_to_md():
    # Загружаем CSV (замени путь на свой файл)
    csv_file = "ratings.csv"
    # df = pd.read_csv(csv_file, delimiter="\t")  # IMDb экспортирует в TSV
    df = pd.read_csv(csv_file, sep=",")  # Указываем, что разделитель — запятая
    # Выбираем нужные столбцы
    columns = {
        "Title": "Title",
        "Year": "Year",
        "IMDb Rating": "IMDb Rating",
        "Your Rating": "Your Rating",
        "Title Type": "Title Type",
        "Genres": "Genres",
        "Num Votes": "Num Votes",
        "Directors": "Directors"
    }

    df = df[list(columns.keys())].rename(columns=columns)

    # TODO: Добавить флаг для форматирования в маркдаун со звёздочками
    # Добавляем звездочки к оценкам
    # df["IMDb Rating"] = df["IMDb Rating"].apply(lambda x: f"{x} ⭐")
    # df["Your Rating"] = df["Your Rating"].apply(lambda x: f"{x} ⭐")

    # Преобразуем в Markdown
    md_table = df.to_markdown(index=False)
    md_table = md_table.replace("|:", "| ").replace(":|", " |").replace(":-", "--")

    # Сохраняем в файл
    with open("imdb_ratings.md", "w", encoding="utf-8") as f:
        f.write(md_table)

    print("✅ Таблица IMDb сохранена в imdb_ratings.md!")

    # TODO: Пофиксить двоеточия в первой стрчоке прим.: |:------
    
def read_markdown_files(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    lines = [line.strip() for line in lines if not set(line.strip()) == {"|",  "-", " "}]
    reader = csv.reader(lines, delimiter="|")
    
    table = [list(map(str.strip, elem[1:-1])) for elem in reader]
    
    headers = table[0]
    rows = table[1:]
    return headers, rows

def get_movie_poster(title, year=None, movie_type=None):
    params = {"t": title, "apikey": API_KEY}
    if year:
        params["y"] = year
    if movie_type:
        params["type"] = movie_type.lower() 
        
    response = requests.get(OMDB_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster")
    
    # Убираем movie_type и пробуем снова
    params.pop("type", None)
    response = requests.get(OMDB_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster")
    
    # Убираем год и пробуем только по названию
    params.pop("y", None)
    response = requests.get(OMDB_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster")
    
    return "None"

def write_markdown_file(output_file, headers, rows):
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["-" * len(h) for h in headers]) + " |"
    
    data_lines = ["| " + " | ".join(row) + " |" for row in rows]
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join([header_line, separator_line] + data_lines) + "\n")

def add_posters_and_save_to_md():
    headers, rows = read_markdown_files(INPUT_MD_FILE)  
    title_index = headers.index("Title")
    year_index = headers.index("Year")
    movie_type_index = headers.index("Title Type")
    headers.insert(headers.index("Title") + 1, "Poster")

    for row in rows:
        title = row[title_index]
        year = row[year_index]
        movie_type = row[movie_type_index]

        poster_url = get_movie_poster(title, year, movie_type)
        row.insert(title_index + 1, f'<img src="{poster_url}" width="100">')

    write_markdown_file(OUTPUT_MD_FILE, headers, rows)  

def fix_broken_posters():
    headers, rows = read_markdown_files(INPUT_MD_FILE)  
    title_index = headers.index("Title")
    poster_index = headers.index("Poster")
    year_index = headers.index("Year")
    movie_type_index = headers.index("Title Type") 
     
    
    for row in rows:
        title = row[title_index]
        year = row[year_index]
        movie_type = row[movie_type_index]

        if "None" in row[poster_index]:
            poster_url = get_movie_poster(title, year, movie_type)
            row[poster_index] = f'<img src="{poster_url}" width="100">'

    write_markdown_file(OUTPUT_MD_FILE, headers, rows)               

# fix_broken_posters()
# add_posters_and_save_to_md()