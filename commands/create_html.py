from lib.create_html import main as create_html

def main(html_name: str, db_path: str, top_n: int) -> int:
    #TODO: Add error handling
    create_html(html_name, db_path, top_n)