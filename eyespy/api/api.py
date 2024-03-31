from fastapi import FastAPI

from api.routers import user
from api.routers import audit
from dal import AuditDal

app = FastAPI()

app.include_router(user.router)
app.include_router(audit.router)

@app.get("/", status_code=200)
def read_root():
    return {"message": "Hello, World!"}
