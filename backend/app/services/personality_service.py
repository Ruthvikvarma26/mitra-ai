from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.personality import Personality
from backend.app.schemas.personality import (
    PersonalityCreate,
    PersonalityUpdate,
)


def create_personality(db: Session, personality: PersonalityCreate):

    existing = db.query(Personality).filter(
        Personality.name == personality.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Personality already exists"
        )

    db_personality = Personality(
        name=personality.name,
        description=personality.description,
        system_prompt=personality.system_prompt,
        voice=personality.voice
    )

    db.add(db_personality)
    db.commit()
    db.refresh(db_personality)

    return db_personality


def get_all_personalities(db: Session):
    return db.query(Personality).all()


def get_personality_by_id(db: Session, personality_id: int):

    personality = db.query(Personality).filter(
        Personality.id == personality_id
    ).first()

    if not personality:
        raise HTTPException(
            status_code=404,
            detail="Personality not found"
        )

    return personality


def update_personality(
    db: Session,
    personality_id: int,
    updated: PersonalityUpdate
):

    personality = get_personality_by_id(db, personality_id)

    personality.name = updated.name
    personality.description = updated.description
    personality.system_prompt = updated.system_prompt
    personality.voice = updated.voice

    db.commit()
    db.refresh(personality)

    return personality


def delete_personality(db: Session, personality_id: int):

    personality = get_personality_by_id(db, personality_id)

    db.delete(personality)
    db.commit()

    return {
        "message": "Personality deleted successfully"
    }