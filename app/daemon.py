import asyncio
import logging
from sqlalchemy.orm import Session
from database.db import SessionLocal, create_card
from utils.call_llm import get_prompt
from models.wordschema import CardSchema, WordSchema
from openai import OpenAI
import os
import json

logger = logging.getLogger(__name__)
client = OpenAI()

INTERVAL_SECONDS = 24 * 60 * 60  # 24 hours


def generate_card(db: Session) -> None:
    prompt = get_prompt(db)
    response = client.responses.create(
        model=os.getenv("MODEL"),
        input=prompt,
    )
    raw = response.output_text  # adjust based on actual OpenAI response shape

    # Expect the LLM to return JSON: {"title": "...", "content": "...", "words": [...]}
    data = json.loads(raw)
    schema = CardSchema(
        title=data["title"],
        content=data.get("content"),
        words=[WordSchema(**w) for w in data["words"]],
    )
    card = create_card(db, schema)
    logger.info(f"Created card: {card.id} — {card.title}")


async def daemon_loop():
    while True:
        db: Session = SessionLocal()
        try:
            generate_card(db)
        except Exception as e:
            logger.error(f"Daemon error: {e}")
        finally:
            db.close()
        await asyncio.sleep(INTERVAL_SECONDS)


def start_daemon():
    asyncio.create_task(daemon_loop())