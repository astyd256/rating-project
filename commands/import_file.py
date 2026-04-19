from pathlib import Path
from lib.import_utils import import_file

ALLOWED_EXTENSIONS = {"csv", "md"}

def main(file_path: str, db_path: str, data_type: str) -> int:

    p = Path(file_path)
    if not p.exists():
        print(f"File not found: {file_path}")
        return 2

    file_ext = p.suffix.lstrip(".").lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        print(f"Unsupported file extension: {file_ext}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
        return 3

    try:
        count = import_file(file_path, db_path, data_type, file_ext)
        print(f"✅ Imported rows: {count}")
        return 0
    except Exception as e:
        print(f"Import error: {e}")
        return 1
