from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from eyespy.api.routers import audit
from eyespy.api.routers import user

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
    "http://localhost:5173/"
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
