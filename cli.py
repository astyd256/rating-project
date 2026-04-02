import argparse
from lib.db_setup import init_db
from commands.import_cmd import main as import_main
from commands.create_html import main as create_html
import os

def ensure_db(path):
    if not os.path.exists(path):
        init_db(path)
        print(f"✅ Database created: {path}")
        
# TODO: Check if needed later and maybe implement
# def db_has_tables(path, tables=("movies", "ratings")):
#     try:
#         with sqlite3.connect(path) as conn:
#             cur = conn.cursor()
#             cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#             existing = {row[0] for row in cur.fetchall()}
#             return all(t in existing for t in tables)
#     except sqlite3.Error:
#         return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ratings CLI")
    parser.add_argument("--init", action="store_true", help="Initialize empty database")
    parser.add_argument("--import-md", type=str, help="Импорт из markdown")
    parser.add_argument("--export-md", type=str, help="Экспорт из markdown")
    parser.add_argument("--db-path", type=str, default="ratings.db", help="Path to SQLite db file")
    parser.add_argument("--html-path", type=str, default="index.html", help="Path to html output file")
    parser.add_argument("--create-html", action="store_true", help="Create html from a database")
    parser.add_argument("--scan-music-metadata", action="store_true", help="Scan metadata from music files to fill out database")
    args = parser.parse_args()

    if args.init:
        ensure_db(args.db_path)

    if args.import_md:
        ensure_db(args.db_path)
        import_main(args.import_md, args.db_path) # TODO: Add proper import flow
        
    if args.create_html:
        ensure_db(args.db_path)
        create_html(args.html_path, args.db_path)
        
    if args.scan_music_metadata:
        ensure_db(args.db_path)
        #TODO Add music tools
        
        
