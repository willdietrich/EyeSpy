from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import users

app = FastAPI()

app.include_router(users.router)

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173"
    "https://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(audit.router)

@app.get("/", status_code=200)
def read_root():
    return {"message": "Hello, World!"}
