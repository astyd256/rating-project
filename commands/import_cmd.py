import sys
from pathlib import Path
from lib.import_utils import import_from_md

def main(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"File not found: {path}")
        return 2
    try:
        count = import_from_md(str(p))
        print(f"Imported rows: {count}")
        return 0
    except Exception as e:
        print(f"Import error: {e}")
        return 1
