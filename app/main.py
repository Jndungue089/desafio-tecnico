from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as leads_router
from app.db.mongodb import connect_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Lead Management API",
    description="API for managing leads with external birth date integration",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(leads_router)
