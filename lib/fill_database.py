import sqlite3
import re
import os

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# Creating table if not exists
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

# Reading markdown data
with open('imdb_ratings.md', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Парсим строки таблицы, пропуская заголовок и разделители
for line in lines[2:]:  # Пропускаем первые две строки (заголовок и разделители)
    line = line.strip()
    if not line or line.startswith('| --'):  # Пропускаем пустые строки и разделители
        continue
    
    # Разделяем строку по вертикальной черте, убираем пустые элементы по краям
    columns = [col.strip() for col in line.split('|')[1:-1]]
    
    # Проверяем, что в строке достаточно данных
    if len(columns) < 9:
        print(f"Пропускаем строку с недостаточным количеством данных: {line}")
        continue
    
    try:
        # Достаем URL из тега <img>
        poster_match = re.search(r'src="([^"]+)"', columns[1])
        poster_url = poster_match.group(1) if poster_match else None

        # Очищаем рейтинги от звезд и других символов
        imdb_rating_clean = re.sub(r'[^0-9.]', '', columns[3].split()[0])
        your_rating_clean = re.sub(r'[^0-9.]', '', columns[4].split()[0])

        # Подготовка данных для вставки
        data = (
            columns[0],                     # title
            poster_url,                     # poster_url
            int(columns[2]),                # year
            float(imdb_rating_clean) if imdb_rating_clean else None,  # imdb_rating
            int(float(your_rating_clean)) if your_rating_clean else None,  # your_rating (преобразуем float в int)
            columns[5],                     # title_type
            columns[6],                     # genres
            int(columns[7].replace(',', '')) if columns[7].replace(',', '').isdigit() else 0,  # num_votes (убираем запятые)
            columns[8]                      # directors
        )

        # Вставляем данные в таблицу
        cursor.execute('''
            INSERT INTO movies (title, poster_url, year, imdb_rating, your_rating, title_type, genres, num_votes, directors)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        
    except (ValueError, IndexError, AttributeError) as e:
        print(f"Ошибка при обработке строки: {line}")
        print(f"Ошибка: {e}")
        continue

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Данные успешно импортированы в базу movies.db")