import os
from typing import List, Optional
from sqlalchemy import create_engine, ForeignKey, String, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session
from models.wordschema import CardSchema

DB_URL = os.environ.get("DB_URL")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL and DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(String(255))
    translation: Mapped[str] = mapped_column(String(255))
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    card: Mapped["Card"] = relationship(back_populates="words")

class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    words: Mapped[List["Word"]] = relationship(
        back_populates="card", 
        cascade="all, delete-orphan",
        lazy="joined"
    )

    @classmethod
    def from_schema(cls, schema: CardSchema) -> "Card":
        return cls(
            title=schema.title,
            words=[Word(**w.model_dump()) for w in schema.words]
        )

Base.metadata.create_all(bind=engine)

def create_card(db: Session, schema: CardSchema) -> Card:
    db_card = Card.from_schema(schema)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_cards(db: Session) -> List[Card]:
    return db.query(Card).all()

def get_latest_card(db: Session) -> Optional[Card]:
    return db.query(Card).order_by(desc(Card.id)).first()

def get_card_by_id(db: Session, card_id: int) -> Optional[Card]:
    return db.query(Card).filter(Card.id == card_id).first()

def delete_card(db: Session, card_id: int) -> bool:
    db_card = get_card_by_id(db, card_id)
    if db_card:
        db.delete(db_card)
        db.commit()
        return True
    return False