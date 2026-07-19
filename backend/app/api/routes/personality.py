from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.core.auth import require_admin
from backend.app.models.user import User
from backend.app.schemas.personality import (
    PersonalityCreate,
    PersonalityUpdate,
    PersonalityResponse,
)
from backend.app.services.personality_service import (
    create_personality,
    get_all_personalities,
    get_personality_by_id,
    update_personality,
    delete_personality,
)

router = APIRouter(
    prefix="/personalities",
    tags=["Personalities"]
)


@router.post("/", response_model=PersonalityResponse)
def create(
    personality: PersonalityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return create_personality(db, personality)


@router.get("/", response_model=list[PersonalityResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_personalities(db)


@router.get("/{personality_id}", response_model=PersonalityResponse)
def get_one(
    personality_id: int,
    db: Session = Depends(get_db)
):
    return get_personality_by_id(db, personality_id)


@router.put("/{personality_id}", response_model=PersonalityResponse)
def update(
    personality_id: int,
    personality: PersonalityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return update_personality(
        db,
        personality_id,
        personality
    )


@router.delete("/{personality_id}")
def delete(
    personality_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return delete_personality(
        db,
        personality_id
    )