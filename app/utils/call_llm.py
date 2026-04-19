from pathlib import Path
from openai import OpenAI
import os
from database.db import get_cards
from sqlalchemy.orm import Session
from models.wordschema import Card

def readfile(path: str) -> str:
    base = Path(__file__).parent
    file_path = base / path
    return file_path.read_text(encoding="utf-8")

def format_cards(cards: list[Card]) -> str:
    lines = []
    for card in cards:
        for w in card.words:
            lines.append(f"{w.word}, {w.translation}")
    return "\n".join(lines)

def get_prompt(db: Session) -> str:
    prompt_text = readfile("../prompts/prompt.md")
    cards_text = format_cards(get_cards(db))
    return f"{prompt_text}\n\n{cards_text}"


client = OpenAI()

response = client.responses.create(
    model=os.getenv("MODEL"),
    input=get_prompt()
)