# EyeSpy

## Finding Something To Do
[The Projects Board](https://github.com/willdietrich/EyeSpy/projects/1) has work in a priority order, grab something from the `To do` column

## Requirements
Install requirements with `pip` using `pip install -r requirements.txt` from the root of the EyeSpy directory

- Python >= 3.10
- Hikari-Py (Discord interaction)
- FastAPI (API backend)
- Uvicorn (API host)
- SQLite 3 (DB)
- Alembic (DB Migration Tool)
- Typescript + React (UI Project)

## Setup
Before running app, run `alembic upgrade head` to migrate the DB

## Arch Diagram
![image](https://user-images.githubusercontent.com/2119242/142131384-ea3d072f-9866-41c7-90ac-7b2f437e76cc.png)

## Building and pushing images
1. Make sure you have logged in using docker login prior to attempting to push or pull images
```docker login registry.walld.me```
2. Build the image
```docker build -t registry.walld.me/wdietrich/eyespy:vXX.XX.XXX```
Where the version is a properly formatted version string
3. Push the image
```docker image push registry.walld.me/wdietrich/eyespy:vXX.XX.XXX```
4. Login to the server and update the compose image with the appropriate new version then reload eyespy
```docker-compose stop eyespy```
```docker-coompose up eyespy```
