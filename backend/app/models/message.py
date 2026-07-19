from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime
from sqlalchemy.sql import func

from backend.app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id")
    )

    sender = Column(String)

    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )