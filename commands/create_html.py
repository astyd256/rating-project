from lib.create_html import main as create_html

def main(html_name: str, db_path: str) -> int:
    #TODO: Add error handling
    create_html(html_name, db_path)