# Rating-project

- [Rating-project](#rating-project)
  - [TL:DR](#tldr)
  - [Service Usage](#service-usage)
  - [Requirements](#requirements)
  - [Features plan](#plan)

## TL:DR
This is my pet-project's tools for working with massive amounts of data for viewed titles, listened music  potentially database backend for a (potentially web) client (and probably my personal blog) for storing rating for games, movies and shows (and probably lots more of staff too)

## Usage
  
**TBA**

## Supported services

- Movies/anime -  [IMDB](https://www.imdb.com/) (partially)
- Steam games - **TBA**
- Music files - **TBA**




## Requirements

- `python-dotenv` - needed for a private OMDB API key. 
*You can use project without it, just need to add your API key inside the code. Probably will add a script argument but no promises.* 😊
- TBA

## Features plan
- [x] **CRITICAL**
  - [x] **Fix proper workflow in cli so it is init db for all data -> html export** 
- [x] Move all wroking tools to one cli
  - [x] Move create_html to cli
- [ ] Finish Readme
- [x] Add license
- [ ] Bake images into html
- [ ] Add Import for:
  - [ ] ~~Markdown files~~
  - [ ] CSV movie list
  - [ ] xml anime/manga list
  - [ ] game (unknown) file
  - [ ] music files mediadata scraping
- [ ] Add Export for:
  - [ ] Markdown files (from universal db/xml)
  - [ ] CSV movie list
  - [ ] xml anime/manga list
  - [ ] game (unknown) file
  - [ ] music files mediadata scraping
- [ ] Add required modules to requirements.txt