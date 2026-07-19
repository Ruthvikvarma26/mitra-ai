from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_user
from backend.app.db.database import get_db
from backend.app.models.user import User

from backend.app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    MessageCreate,
    MessageResponse,
    ChatRename,
)

from backend.app.services.chat_service import (
    create_chat_session,
    chat_with_personality,
    get_user_chat_sessions,
    get_chat_messages,
    rename_chat_session,
    delete_chat_session,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/session",
    response_model=ChatSessionResponse
)
def create_session(
    session: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_chat_session(
        db=db,
        user_id=current_user.id,
        personality_id=session.personality_id,
        title=session.title
    )


@router.get(
    "/sessions",
    response_model=list[ChatSessionResponse]
)
def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_chat_sessions(
        db=db,
        user_id=current_user.id
    )


@router.post("/{session_id}/message")
def send_message(
    session_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_with_personality(
        db=db,
        session_id=session_id,
        user_message=message.message
    )


@router.get(
    "/{session_id}/messages",
    response_model=list[MessageResponse]
)
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_chat_messages(
        db=db,
        session_id=session_id
    )
@router.put(
    "/{session_id}/rename",
    response_model=ChatSessionResponse
)
def rename_chat(
    session_id: int,
    data: ChatRename,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return rename_chat_session(
        db=db,
        session_id=session_id,
        title=data.title,
    )

@router.delete("/{session_id}")
def delete_chat(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_chat_session(
        db=db,
        session_id=session_id
    )