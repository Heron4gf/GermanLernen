import asyncio
import logging
from sqlalchemy.orm import Session
from database.db import SessionLocal, create_card
from utils.call_llm import generate_card_schema

logger = logging.getLogger(__name__)

INTERVAL_SECONDS = 24 * 60 * 60


def run_generation() -> None:
    logger.info("Daemon tick — starting card generation")
    db: Session = SessionLocal()
    try:
        schema = generate_card_schema(db)
        logger.info(f"LLM returned schema: title={schema.title!r}, words={len(schema.words)}")
        card = create_card(db, schema)
        logger.info(f"Card created successfully: id={card.id} title={card.title!r}")
    except Exception as e:
        logger.error(f"Daemon error during generation: {e}", exc_info=True)
    finally:
        db.close()


async def daemon_loop():
    logger.info(f"Daemon loop started — interval={INTERVAL_SECONDS}s ({INTERVAL_SECONDS // 3600}h)")
    while True:
        await asyncio.get_event_loop().run_in_executor(None, run_generation)
        logger.info(f"Daemon sleeping for {INTERVAL_SECONDS}s until next generation")
        await asyncio.sleep(INTERVAL_SECONDS)


def start_daemon():
    asyncio.create_task(daemon_loop())
