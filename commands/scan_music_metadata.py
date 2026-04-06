from lib.scan_music_metadata import main as scan_music_metadata
def main(music_folder_path: str, db_path: str, top_n: int, block_no_star_music: bool) -> int:
    #TODO: Add error handling
    print(f"Starting music scanning")
    music_count = scan_music_metadata(music_folder_path, db_path, top_n, block_no_star_music)
    print(f"✅ Music scanned: {music_count} new tracks added")