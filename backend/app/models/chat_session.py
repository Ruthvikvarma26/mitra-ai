from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    personality_id = Column(
        Integer,
        ForeignKey("personalities.id")
    )