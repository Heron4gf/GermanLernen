import asyncio
import logging
from sqlalchemy.orm import Session
from backend.app.database.db import SessionLocal, create_card
from backend.app.utils.call_llm import generate_card_schema

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 24 * 60 * 60


def run_generation(db: Session) -> None:
    schema = generate_card_schema(db)
    card = create_card(db, schema)
    logger.info(f"Created card: {card.id} — {card.title}")


async def daemon_loop():
    while True:
        db: Session = SessionLocal()
        try:
            run_generation(db)
        except Exception as e:
            logger.error(f"Daemon error: {e}", exc_info=True)
        finally:
            db.close()
        await asyncio.sleep(INTERVAL_SECONDS)


def start_daemon():
    asyncio.create_task(daemon_loop())