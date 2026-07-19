from sqlalchemy.orm import Session

from backend.app.models.chat_session import ChatSession
from backend.app.models.message import Message

from backend.app.models.personality import Personality
from backend.app.services.ai_service import generate_reply

from fastapi import HTTPException

def create_chat_session(
    db: Session,
    user_id: int,
    personality_id: int,
    title: str | None = None
):
    session = ChatSession(
        user_id=user_id,
        personality_id=personality_id,
        title=title
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def save_message(
    db: Session,
    session_id: int,
    sender: str,
    message: str
):
    msg = Message(
        session_id=session_id,
        sender=sender,
        message=message
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return msg

def chat_with_personality(
    db: Session,
    session_id: int,
    user_message: str
):
    if not user_message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
        
    # Save user's message
    save_message(
        db=db,
        session_id=session_id,
        sender="user",
        message=user_message
    )

    # Get chat session
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )
    # Get personality
    personality = db.query(Personality).filter(
        Personality.id == session.personality_id
    ).first()

    if not personality:
        raise HTTPException(
            status_code=404,
            detail="Personality not found"
        )
    # Generate AI reply
    ai_reply = generate_reply(
        personality.system_prompt,
        user_message
    )

    # Save AI reply
    save_message(
        db=db,
        session_id=session_id,
        sender="assistant",
        message=ai_reply
    )

    return {
        "reply": ai_reply
    }

def get_user_chat_sessions(
    db: Session,
    user_id: int
):
    return (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .all()
    )

def get_chat_messages(
    db: Session,
    session_id: int,
    user_id: int
):
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )

def rename_chat_session(
    db: Session,
    session_id: int,
    user_id: int,
    title: str
):
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    session.title = title

    db.commit()
    db.refresh(session)

    return session

def delete_chat_session(
    db: Session,
    session_id: int,
    user_id: int
):
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    db.query(Message).filter(
        Message.session_id == session_id
    ).delete()

    db.delete(session)
    db.commit()

    return {
        "success": True,
        "message": "Chat deleted successfully"
    }