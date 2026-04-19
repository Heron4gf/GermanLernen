from contextlib import asynccontextmanager
from fastapi import FastAPI
from router.v1 import router as v1_router
from daemon import start_daemon

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_daemon()
    yield

app = FastAPI(title="Card API", version="1.0.0", lifespan=lifespan)
app.include_router(v1_router)