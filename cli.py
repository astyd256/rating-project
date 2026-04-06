import argparse
from lib.db_setup import init_db
from commands.import_md import main as import_md
from commands.create_html import main as create_html
from commands.scan_music_metadata import main as scan_music_metadata
import os

def ensure_db(path):
    if not os.path.exists(path):
        init_db(path)
        print(f"✅ Database created: {path}")
    # TODO: Add creating db tables
        
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
    parser = argparse.ArgumentParser(
        description=(
            "Ratings CLI\n\n"
            
            ""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--init", action="store_true", help="Initialize empty database")
    parser.add_argument("--import-md", type=str, help="Import from markdown(working only with movies now)")
    parser.add_argument("--export-md", type=str, help="Export to markdown")
    parser.add_argument("--create-html", action="store_true", help="Create html from a database")
    parser.add_argument("--scan-music-metadata", type=str, help="Scan metadata from music files to fill out database")
    
    parser.add_argument("--db-path", type=str, default="ratings.db", help="Path to SQLite db file")
    parser.add_argument("--html-path", type=str, default="index.html", help="Path to html output file")
    parser.add_argument("--top-n", type=int, default = 50, help = "Limit to number of things rated (for now)")
    parser.add_argument("--block-no-star-music", type=bool, default = True, help = "Used to scrap music without rating")
    args = parser.parse_args()

    if args.init:
        ensure_db(args.db_path)

    if args.import_md:
        ensure_db(args.db_path)
        import_md(args.import_md, args.db_path) # TODO: Add proper import flow
        
    if args.create_html:
        ensure_db(args.db_path)
        create_html(args.html_path, args.db_path, args.top_n)
        
    if args.scan_music_metadata:
        ensure_db(args.db_path)
        scan_music_metadata(args.scan_music_metadata, args.db_path, args.top_n, args.block_no_star_music)
        #TODO Add music tools
        
        
