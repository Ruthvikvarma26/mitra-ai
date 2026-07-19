from datetime import datetime
from pydantic import BaseModel


# ---------- Chat Session ----------

class ChatSessionCreate(BaseModel):
    personality_id: int
    title: str | None = None


class ChatSessionResponse(BaseModel):
    id: int
    title: str | None
    user_id: int
    personality_id: int

    class Config:
        from_attributes = True


# ---------- Messages ----------

class MessageCreate(BaseModel):
    message: str


class MessageResponse(BaseModel):
    id: int
    session_id: int
    sender: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRename(BaseModel):
    title: str