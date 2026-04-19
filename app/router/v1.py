from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db, get_cards, get_latest_card
from models.wordschema import CardResponse

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/latest", response_model=CardResponse)
def get_latest(db: Session = Depends(get_db)):
    card = get_latest_card(db)
    if card is None:
        raise HTTPException(status_code=404, detail="No cards found")
    return CardResponse.from_orm_card(card)


@router.get("", response_model=list[CardResponse])
def get_card_list(db: Session = Depends(get_db)):
    cards = get_cards(db)
    return [CardResponse.from_orm_card(c) for c in cards]