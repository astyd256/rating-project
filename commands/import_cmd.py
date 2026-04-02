from pathlib import Path
from lib.import_utils import import_from_md

def main(file_path: str, db_path: str) -> int:
    fp = Path(file_path)
    dbp = Path(db_path)
    if not fp.exists():
        print(f"File not found: {fp}")
        return 2
    # if not dbp.exists():
    #     print(f"DB not found: {dbp}")
    #     return 2
    try:
        count = import_from_md(file_path, db_path)
        print(f"✅ Imported rows: {count}")
        return 0
    except Exception as e:
        print(f"Import error: {e}")
        return 1
