from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace

from eyespy.api.routers import audit
from eyespy.api.routers import user

tracer = trace.get_tracer("eyespy.api.tracer")

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
    "http://localhost:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(audit.router)

@app.get("/", status_code=200)
def read_root():
    message = "Hello, World!"
    with tracer.start_as_current_span("read_root") as span:
        span.set_attribute("message", message)
        return {"message": message}

@app.get("/rehydrate", status_code=200)
def read_root():
    message = "Hello, World!"
    with tracer.start_as_current_span("read_root") as span:
        span.set_attribute("message", message)
        return {"message": message}
