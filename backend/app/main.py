import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from router.v1 import router as v1_router
from daemon import start_daemon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup — launching daemon")
    start_daemon()
    yield
    logger.info("Application shutdown")


app = FastAPI(title="Card API", version="1.0.0", lifespan=lifespan)
app.include_router(v1_router)
