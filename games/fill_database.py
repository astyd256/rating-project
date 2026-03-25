import sqlite3
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote

# Функция для извлечения данных из HTML
def extract_data_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Находим таблицу с id="table-apps"
    table = soup.find('table', {'id': 'table-apps'})
    if not table:
        print("Таблица не найдена")
        return []
    
    # Находим все тела таблицы (tbody)
    tbodies = table.find_all('tbody')
    results = []
    
    for tbody in tbodies:
        # Извлекаем название игры
        name_link = tbody.find('td', class_='text-left').find('a')
        game_name = name_link.get_text(strip=True) if name_link else "Неизвестно"
        
        # Извлекаем изображение
        img_tag = tbody.find('td', class_='applogo').find('img')
        img_src = img_tag['src'] if img_tag and img_tag.has_attr('src') else ""
        # Декодируем URL и извлекаем имя файла
        img_filename = os.path.basename(unquote(img_src)) if img_src else ""
        
        # Извлекаем рейтинг (последний td с классом dt-type-numeric)
        rating_cells = tbody.find_all('td', class_='dt-type-numeric')
        rating = rating_cells[-1].get_text(strip=True).replace('%', '') if rating_cells else "0"
        
        # Добавляем в результаты
        if game_name != "Неизвестно":
            results.append({
                'game_name': game_name,
                'image_filename': img_filename,
                'rating': float(rating) if rating.replace('.', '').isdigit() else 0,
                'my_rating': None  # Пустое значение для вашего рейтинга
            })
    
    return results

# Функция для создания и заполнения базы данных
def create_database(data, db_name='games.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Создаем таблицу
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name TEXT NOT NULL,
        image_filename TEXT,
        rating REAL,
        my_rating REAL
    )
    ''')
    
    # Вставляем данные
    for item in data:
        cursor.execute('''
        INSERT INTO games (game_name, image_filename, rating, my_rating)
        VALUES (?, ?, ?, ?)
        ''', (item['game_name'], item['image_filename'], item['rating'], item['my_rating']))
    
    conn.commit()
    conn.close()

# Основная логика
if __name__ == "__main__":
    html_file = "ваш_файл.htm"  # Укажите путь к вашему HTML-файлу
    data = extract_data_from_html(html_file)
    
    if data:
        create_database(data)
        print(f"Успешно добавлено {len(data)} записей в базу данных")
    else:
        print("Не удалось извлечь данные из файла")