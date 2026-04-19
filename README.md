# Rating-project

  - [TL:DR](#tldr)
  - [Usage](#usage)
  - [Supported services](#supported-services)
  - [Features](#features)

## TL:DR
This is my pet-project's tools for working with massive amounts of data for viewed titles, listened music  potentially database backend for a (potentially web) client (and probably my personal blog) for storing rating for games, movies and shows (and probably lots more of staff too)

## Usage

Create and activate a virtual environment, install dependencies, then run the CLI:

- macOS / Linux (bash/zsh):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python cli.py --help
```

- Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python cli.py --help
```

Notes:
- **Python version:** 3.11+
- To deactivate the venv: `deactivate`

## Supported services

- Movies/anime - ~~[IMDB](https://www.imdb.com/)~~ - broken again ([partially](./examples/imdb_ratings.md))
- Steam games - **TBA**
- Music files - **WIP**

## Features
-  **CLI functionality**
- [ ] **Bake images into html** (hope will work for metadata for now)
- [ ] Change license 
  - [x] music bee mp3 image metadata
  - [x] FLAC
- [ ] DB:
  - [x] Add DB interface (SQLALchemy)
  - [ ] Migrations
- [ ] Import:
  - [ ] Movies
    - [x] Markdown [exmaple](./examples/imdb_ratings.md)
      - [ ] **Fix posters**
    - [ ] CSV (IMDB format)
  - [ ] Anime/Manga
    - [ ] xml
  - [ ] game (unknown)
  - [x] music files mediadata scraping
  - [ ] ANY
    - [ ] JSON files
- [ ] Export:
  - [ ] Markdown?
  - [ ] Html site
    - [ ] **Add lazy loading**
    - [ ] Make it less hardcoded
  - [ ] JSON
  - [ ] CSV (IMDB format)
  - [ ] xml anime/manga (MAL format)
  - [ ] games (unknown format)
- [ ] CLI UI interface