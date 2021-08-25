from fastapi import FastAPI

from api.routers import users

app = FastAPI()

app.include_router(users.router)


@app.get("/", status_code=200)
def read_root():
    return {"message": "Hello, World!"}
