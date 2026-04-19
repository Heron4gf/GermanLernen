import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.v1 import router as v1_router
from daemon import start_daemon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

_cors_origin = os.environ.get("CORS_ORIGIN", "http://localhost:2372")
ALLOWED_ORIGINS = [o.strip() for o in _cors_origin.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup — launching daemon")
    logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")
    start_daemon()
    yield
    logger.info("Application shutdown")


app = FastAPI(title="Card API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
