from __future__ import annotations
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pydantic import BaseModel

class WordSchema(BaseModel):
    word: str
    translation: str

class CardSchema(BaseModel):
    title: str
    words: List[WordSchema]

class Base(DeclarativeBase):
    pass

class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    words: Mapped[List[Word]] = relationship(back_populates="card", cascade="all, delete-orphan")

    @classmethod
    def from_schema(cls, schema: CardSchema) -> Card:
        return cls(
            title=schema.title,
            words=[Word(**w.model_dump()) for w in schema.words]
        )

class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(255))
    translation: Mapped[str] = mapped_column(String(255))
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped[Card] = relationship(back_populates="words")