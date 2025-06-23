import argparse
from db_setup import init_db
from import_utils import import_from_md, import_from_excel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Movie DB CLI")
    parser.add_argument("--init", action="store_true", help="Инициализировать БД")
    parser.add_argument("--import-md", type=str, help="Импорт из markdown")
    parser.add_argument("--export-md", type=str, help="Импорт из markdown")
    args = parser.parse_args()

    if args.init:
        init_db()
        print("✅ База данных инициализирована.")

    if args.import_md:
        import_from_md(args.import_md)
