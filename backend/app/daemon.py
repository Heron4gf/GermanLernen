import asyncio
import logging
from sqlalchemy.orm import Session
from database.db import SessionLocal, create_card
from utils.call_llm import generate_card_schema

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 24 * 60 * 60


def run_generation() -> None:
    db: Session = SessionLocal()
    try:
        schema = generate_card_schema(db)
        card = create_card(db, schema)
        logger.info(f"Created card: {card.id} — {card.title}")
    except Exception as e:
        logger.error(f"Daemon error: {e}", exc_info=True)
    finally:
        db.close()


async def daemon_loop():
    # Run immediately on startup, then every 24h
    while True:
        await asyncio.get_event_loop().run_in_executor(None, run_generation)
        await asyncio.sleep(INTERVAL_SECONDS)


def start_daemon():
    asyncio.create_task(daemon_loop())