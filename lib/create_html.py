import sqlite3
import webbrowser
from pathlib import Path

# Подключаемся к базе
DB_PATH = "movies.db" #TODO add one path variable
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Выбираем все фильмы
cursor.execute('SELECT * FROM movies ORDER BY your_rating DESC')
movies = cursor.fetchall()
conn.close()

# Генерируем HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Movie Collection</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .movie-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding: 20px;
        }
        .movie-card {
            width: 200px;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .movie-card img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>My Movie Collection</h1>
    <div class="movie-container">
"""

for movie in movies:
    # movie[0] - id, movie[1] - title, movie[2] - poster_url, etc.
    html_content += f"""
        <div class="movie-card">
            <h3>{movie[1]} ({movie[3]})</h3>
            <img src="{movie[2]}" alt="{movie[1]} Poster" onerror="this.style.display='none'">
            <p><b>My Rating:</b> {movie[5]} / 10</p>
            <p><b>IMDb:</b> {movie[4]} / 10</p>
            <p><b>Genres:</b> {movie[7]}</p>
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# Сохраняем HTML файл
file_path = "ratings.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Открываем в браузере
webbrowser.open(file_path)