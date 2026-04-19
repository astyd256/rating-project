import argparse
from lib.db.init import init_db
from commands.import_file import main as import_file
from commands.create_html import main as create_html
from commands.scan_music_metadata import main as scan_music_metadata
import os

def ensure_db(path):
    if not os.path.exists(path):
        init_db(path)
        print(f"✅ Database created: {path}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Ratings CLI\n\n"
            
            ""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--init", action="store_true", help="Initialize empty database")
    parser.add_argument("--import-file", type=str, help="Import from markdown(working only with movies now)")
    parser.add_argument("--export-md", type=str, help="Export to markdown")
    parser.add_argument("--create-html", action="store_true", help="Create html from a database")
    parser.add_argument("--scan-music-metadata", type=str, help="Scan metadata from music files to fill out database")
    
    parser.add_argument("--db-path", type=str, default="ratings.db", help="Path to SQLite db file")
    parser.add_argument("--html-path", type=str, default="index.html", help="Path to html output file")
    parser.add_argument("--data-type", type=str, default="movie", help="Type of the data inside file")
    parser.add_argument("--top-n", type=int, default = 50, help = "Limit to number of things rated (for now)")
    parser.add_argument("--block-no-star-music", type=bool, default = True, help = "Used to scrap music without rating")
    
    args = parser.parse_args()

    if args.init:
        ensure_db(args.db_path)

    if args.import_file:
        ensure_db(args.db_path)
        import_file(args.import_file, args.db_path, args.data_type) # TODO: Add proper import flow
        
    if args.create_html:
        ensure_db(args.db_path)
        create_html(args.html_path, args.db_path, args.top_n)
        
    if args.scan_music_metadata:
        ensure_db(args.db_path)
        #Rewrite to db interface
        scan_music_metadata(args.scan_music_metadata, args.db_path, args.top_n, args.block_no_star_music)
        
        
