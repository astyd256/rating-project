import os
import json
import sqlite3
from typing import Optional, List, Dict, Tuple
from mutagen import File as MutagenFile
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from PIL import Image
from io import BytesIO

SUPPORTED_EXT = {'.mp3', '.flac', '.m4a', '.mp4', '.wav', '.ogg', '.opus', '.aac'}

def _first_of(v):
    if v is None:
        return None
    # mutagen ID3 frame (has .text) -> взять первый текст
    text = getattr(v, 'text', None)
    if text is not None:
        return text[0] if isinstance(text, (list, tuple)) and text else text
    # обычный список/кортеж
    if isinstance(v, (list, tuple)):
        return v[0] if v else None
    # строка или число
    return v


def _safe_tag_value(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        out = []
        for item in v:
            if hasattr(item, 'text'):
                try:
                    out.append(item.text)
                except Exception:
                    out.append(str(item))
            else:
                out.append(item)
        return out
    if hasattr(v, 'text'):
        try:
            return v.text
        except Exception:
            return str(v)
    return str(v)


def _parse_rating_from_tags(tags) -> Optional[int]:
    if tags is None:
        return None
    # try common keys
    candidates = []
    for key in ('POPM', 'rating', 'RATING', 'WM/PRATING', 'REPLAYGAIN_RATING'):
        if key in tags:
            v = _first_of(tags.get(key))
            if v is None:
                continue
            try:
                iv = float(v)
                candidates.append(iv)
            except Exception:
                s = str(v)
                if '/' in s:
                    try:
                        a, b = s.split('/', 1)
                        candidates.append(round(int(a) / int(b) * 5), 2)
                    except Exception:
                        pass
                elif s.endswith('%'):
                    try:
                        p = float(s.strip('%'))
                        candidates.append(round(p / 100.0 * 5), 2)
                    except Exception:
                        pass
                else:
                    # try float
                    try:
                        fv = float(s)
                        candidates.append(int(round(fv)))
                    except Exception:
                        pass
    if not candidates:
        return None
    # choose first reasonable mapped to 0..5
    for v in candidates:
        if 0 <= v <= 5:
            return v
        if v <= 100:
            return (v / 100.0) * 5.0
        if v <= 255:
            return (v / 255.0) * 5.0
    return None


def _try_convert_image_to_png(image_bytes: bytes) -> bytes:
    try:
        img = Image.open(BytesIO(image_bytes))
        out = BytesIO()
        img.save(out, format='PNG')
        return out.getvalue()
    except Exception:
        return image_bytes

def compress_album_art(apic_data, max_size=200, quality=75, fmt='WEBP'):
    try:
        img = Image.open(BytesIO(apic_data)).convert('RGBA')
    except Exception:
        return apic_data

    img.thumbnail((max_size, max_size), Image.LANCZOS)
    
    out = BytesIO()
    if fmt.upper() == 'JPEG':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])  # альфа как маска
        bg.save(out, format='JPEG', quality=quality, optimize=True)
    else:
        # WebP поддерживает альфу
        img.save(out, format=fmt.upper(), quality=quality, method=6)
    return out.getvalue()

def _extract_metadata(filepath: str) -> Tuple[Optional[bytes], Dict]:
    """
    Возвращает (album_art_bytes_or_None, metadata_dict)
    metadata_dict содержит: title, album, artist, rating (0..5 or None), raw_tags
    """
    metadata = {}
    audio = MutagenFile(filepath, easy=False)
    title = None
    album = None
    artist = None
    rating = None
    album_art_bytes = None

    # Try format-specific extraction
    try:
        low = filepath.lower()
        # MP3 ID3
        if low.endswith('.mp3'):
            try:
                tags = ID3(filepath)
                title = _first_of(tags.get('TIT2').text) if tags.get('TIT2') else None
            except Exception:
                tags = getattr(audio, 'tags', None)
            try:
                if tags:
                    # APIC frames (album art)
                    apics = tags.getall('APIC') if hasattr(tags, 'getall') else None
                    if apics:
                        album_art_bytes = compress_album_art(apics[0].data)
                    # POPM (rating)
                    # PROBABLY ONLY WORKS WITH POPM:MusicBee, consider adding other support
                    for key in list(tags.keys()):
                        if key.upper().startswith('POPM'):
                            popm = tags.get(key)
                            if popm is None:
                                continue
                            if isinstance(popm, (list, tuple)):
                                popm = popm[0] if popm else None
                            if popm is None:
                                continue
                            try:
                                r = getattr(popm, 'rating', None)
                                if r is None:
                                    r = float(popm)
                                else:
                                    r = float(r)
                            except Exception:
                                continue
                            if r < 0:
                                rating = None
                            # POPM — 0..255
                            if r <= 255:
                                rating = round((r / 255.0) * 5.0, 2)
                    if title is None:
                        title = _first_of(tags.get('TIT2')) if hasattr(tags, 'get') else None
                    album = album or (_first_of(tags.get('TALB')) if hasattr(tags, 'get') else None)
                    artist = artist or (_first_of(tags.get('TPE1')) if hasattr(tags, 'get') else None)
            except Exception:
                pass

        # FLAC
        if low.endswith('.flac') or isinstance(audio, FLAC):
            try:
                tags = getattr(audio, 'tags', None)
                if tags:
                    title = title or _first_of(tags.get('TITLE'))
                    album = album or _first_of(tags.get('ALBUM'))
                    artist = artist or _first_of(tags.get('ARTIST'))
                    rating = rating or _parse_rating_from_tags(tags)
                pics = getattr(audio, 'pictures', None)
                if pics:
                    album_art_bytes = pics[0].data
            except Exception:
                pass

        # MP4/M4A
        if low.endswith(('.m4a', '.mp4', '.aac')):
            try:
                tags = getattr(audio, 'tags', None)
                if tags:
                    title = title or _first_of(tags.get('\xa9nam'))
                    album = album or _first_of(tags.get('\xa9alb'))
                    artist = artist or _first_of(tags.get('\xa9ART'))
                    covr = tags.get('covr')
                    if covr:
                        album_art_bytes = covr[0]
                    rating = rating or _parse_rating_from_tags(tags)
            except Exception:
                pass

        # Generic easy tags fallback
        try:
            easy = MutagenFile(filepath, easy=True)
            if easy is not None:
                title = title or _first_of(easy.get('title')) or os.path.splitext(os.path.basename(filepath))[0]
                album = album or _first_of(easy.get('album'))
                artist = artist or _first_of(easy.get('artist')) or _first_of(easy.get('albumartist'))
                rating = rating or _parse_rating_from_tags(easy)
        except Exception:
            pass

    except Exception:
        pass

    metadata['title'] = title or os.path.splitext(os.path.basename(filepath))[0]
    metadata['album'] = album
    metadata['artist'] = artist
    metadata['rating'] = rating

    # raw tags
    raw_tags = {}
    try:
        if getattr(audio, 'tags', None) is not None:
            for k, v in audio.tags.items():
                try:
                    raw_tags[str(k)] = _safe_tag_value(v)
                except Exception:
                    raw_tags[str(k)] = None
    except Exception:
        raw_tags = {}
    metadata['raw_tags'] = raw_tags

    return album_art_bytes, metadata


def main(music_folder_path: str, db_path: str, top_n: int, block_no_star_music: bool) -> int:
    """
    Scans folder recursive, checks metadata from all audiofiles.
    top_n: if >0 — saves only top_n tracks with highest rating;
           if <=0 — save all tracks.
    block_no_star_music: True — skip all tracks with rating == None.
    Returns number of saved records.
    """
    #TODO: It could be unoptimized in terms of limit because we check all files anyway and sort all files anyway too
    # Should be ok for few hundreds / thousands
    entries: List[Dict] = []

    for root, _, files in os.walk(music_folder_path):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SUPPORTED_EXT:
                continue
            full = os.path.join(root, fname)
            try:
                album_art_bytes, meta = _extract_metadata(full)
                if block_no_star_music and (meta.get('rating') is None):
                    continue
                entries.append({
                    'path': full,
                    'album_art_bytes': album_art_bytes,
                    'title': meta.get('title'),
                    'album': meta.get('album'),
                    'artist': meta.get('artist'),
                    'rating': meta.get('rating')
                })
            except Exception:
                continue

    # If top_n > 0 — then we sort and adding only top_n music tracks
    if top_n and top_n > 0:
        # Sort by rating desc (None -> -1), then by title asc for determinism
        def sort_key(e):
            r = e['rating']
            r_key = r if r is not None else -1
            t = e['title'] or ''
            return (-r_key, t)
        entries.sort(key=sort_key)
        entries = entries[:top_n]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    saved = 0
    for e in entries:
        try:
            album_art_blob = None
            if e['album_art_bytes']:
                album_art_blob = sqlite3.Binary(_try_convert_image_to_png(e['album_art_bytes']))
            cursor.execute('''
                INSERT INTO music (title, album, artist, album_art, rating)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                e['title'],
                e['album'],
                e['artist'],
                album_art_blob,
                e['rating']
            ))
            saved += 1
        except Exception:
            continue
    conn.commit()
    conn.close()
    return saved
