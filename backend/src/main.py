from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.core.config import settings
from src.core.database import Base, engine
from src.core.schema_sync import ensure_schema
from src.models import entities  # noqa: F401

app = FastAPI(title=settings.app_name, docs_url="/docs")

origins = [
    "http://localhost:5173",  # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/test")
def test():
    return {"message": "CORS works"}


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_schema(engine)


app.include_router(api_router, prefix=settings.api_prefix)
