# Rating-project

- [TL:DR](#tldr)
- [Usage](#usage)
- [Requirements](#requirements)
- [Features plan](#plan)

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




## Requirements



## Features
-  **CLI functions**
-  Creating html site from db data 
-  Movies .md specific format import [exmaple](./examples/imdb_ratings.md) (was hoping to add it all to obsidian but the idea is scraped now, maybe will come back to it later):
- [x] **Bake images into html** (hope will work for metadata for now)
  - [ ] Works with
- [ ] **ADD DB Interface FOR MIGRATION** (Django)
- [ ] Add Import for:
  - [ ] ~~Markdown files~~
  - [ ] JSON files
  - [ ] CSV movie list
  - [ ] xml anime/manga list
  - [ ] game (unknown) files
  - [x] music files mediadata scraping
- [ ] Add Export for:
  - [ ] JSON format
  - [ ] Markdown files (from universal db/xml)
  - [ ] CSV movie list
  - [ ] xml anime/manga list
  - [ ] game (unknown) files
- [ ] Add type (music, game, etc) export/import
- [ ] Add required modules to requirements.txt
- [ ] CLI UI interface
- [ ] Re add converter IMDB .csv to .md from tools 
- [ ] Add doc
- [ ] Finish Readme