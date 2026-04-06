import sqlite3
import base64
import json
from html import escape

def main(html_name: str, db_path: str, top_n: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ----MOVIES----
    cursor.execute('SELECT * FROM movies ORDER BY rating DESC')
    movies = cursor.fetchall()

    # ----MUSIC: только с album_art (не NULL и не пустой)----
    cursor.execute('''
        SELECT * FROM music
        WHERE album_art IS NOT NULL AND LENGTH(album_art) > 0
        ORDER BY rating DESC
    ''')
    music_rows = cursor.fetchall()

    conn.close()

    def album_art_data_uri(blob_bytes):
        if not blob_bytes:
            return None
        b64 = base64.b64encode(blob_bytes).decode('ascii')
        return f"data:image/jpeg;base64,{b64}"  # предполагаем jpeg; если PNG — можно детектировать

    # HTML generation
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>My Collection</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .tabs {{
                display:flex;
                gap:8px;
                margin-bottom:16px;
            }}
            .tab-btn {{
                padding:8px 12px;
                border-radius:6px;
                border:1px solid #ccc;
                background:#fff;
                cursor:pointer;
            }}
            .tab-btn.active {{
                background:#222;
                color:#fff;
            }}
            .section {{ display:none; }}
            .section.active {{ display:block; }}

            .container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                padding: 10px 0;
                align-items: flex-start;
            }}

            .card {{
                width: 200px;
                border: 1px solid #ccc;
                padding: 12px;
                border-radius: 5px;
                text-align: center;
                background: #fff;
                display:flex;
                flex-direction:column;
                align-items:center;
                min-height: 456.666px;
            }}

            .card h3 {{
                margin: 0 0 8px 0;
                font-size: 15px;
                line-height: 1.2;
                height: 2.4em;
                overflow: hidden;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
            }}

            .card img {{
                width: 100%;
                height: auto;
                margin-bottom: 10px;
                object-fit: cover;
                display:block;
                border-radius:3px;
            }}

            .card p {{ margin:6px 0; font-size:13px; color:#222; }}
            @media (max-width:520px) {{ .card {{ width:48%; }} }}
            @media (max-width:360px) {{ .card {{ width:100%; }} }}
        </style>
    </head>
    <body>
        <h1>My Collection</h1>

        <div class="tabs">
            <button class="tab-btn active" data-target="movies">Movies</button>
            <button class="tab-btn" data-target="music">Music</button>
        </div>

        <div id="movies" class="section active">
            <div class="container">
    """

    # Movies section (limit top_n)
    limit = 0
    for movie in movies:
        title = escape(str(movie[1])) if movie[1] is not None else ""
        poster = escape(str(movie[2])) if movie[2] is not None else ""
        year = escape(str(movie[3])) if len(movie) > 3 and movie[3] is not None else ""
        imdb = escape(str(movie[4])) if len(movie) > 4 and movie[4] is not None else ""
        myrating = escape(str(movie[5])) if len(movie) > 5 and movie[5] is not None else ""
        genres = escape(str(movie[7])) if len(movie) > 7 and movie[7] is not None else ""

        html_content += f"""
                <div class="card">
                    <h3>{title} ({year})</h3>
                    <img src="{poster}" alt="{title} Poster" onerror="this.style.display='none'">
                    <p><b>My Rating:</b> {myrating} / 10</p>
                    <p><b>IMDb:</b> {imdb} / 10</p>
                    <p><b>Genres:</b> {genres}</p>
                </div>
        """
        limit += 1
        if limit == top_n:
            break

    html_content += """
            </div>
        </div>

        <div id="music" class="section">
            <div class="container">
    """

    # Music section (limit top_n)
    limit = 0
    for m in music_rows:
        # music schema: id, title, album, artist, album_art (bytes), rating, metadata_json
        m_id = m[0]
        m_title = escape(str(m[1])) if m[1] is not None else ""
        m_album = escape(str(m[2])) if m[2] is not None else ""
        m_artist = escape(str(m[3])) if m[3] is not None else ""
        m_album_art_blob = m[4]
        m_rating = escape(str(m[5])) if len(m) > 5 and m[5] is not None else ""

        data_uri = album_art_data_uri(m_album_art_blob)
        img_tag = f'<img src="{data_uri}" alt="{m_title} Album Art">' if data_uri else ''

        html_content += f"""
                <div class="card">
                    <h3>{m_title}</h3>
                    {img_tag}
                    <p><b>Artist:</b> {m_artist}</p>
                    <p><b>Album:</b> {m_album}</p>
                    <p><b>Rating:</b> {m_rating}</p>
                </div>
        """
        limit += 1
        if limit == top_n:
            break

    html_content += """
            </div>
        </div>

        <script>
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                    btn.classList.add('active');
                    document.getElementById(btn.dataset.target).classList.add('active');
                });
            });
        </script>
    </body>
    </html>
    """

    with open(html_name, "w", encoding="utf-8") as f:
        f.write(html_content)
