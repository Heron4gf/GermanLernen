from pathlib import Path
from openai import OpenAI
from sqlalchemy.orm import Session
from backend.app.database.db import get_cards
from backend.app.models.wordschema import CardSchema
import os

client = OpenAI()


def _read_prompt_template() -> str:
    base = Path(__file__).parent
    return (base / "../prompts/prompt.md").read_text(encoding="utf-8")


def _format_cards(cards) -> str:
    lines = []
    for card in cards:
        for w in card.words:
            lines.append(f"{w.word}, {w.translation}")
    return "\n".join(lines)


def generate_card_schema(db: Session) -> CardSchema:
    system_prompt = _read_prompt_template()
    existing_words = _format_cards(get_cards(db))

    response = client.responses.parse(
        model=os.getenv("MODEL"),
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Already used words:\n{existing_words}"},
        ],
        text_format=CardSchema,
    )

    return response.output_parsed