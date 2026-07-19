from sqlalchemy import Column, Integer, String, Text

from backend.app.db.database import Base


class Personality(Base):
    __tablename__ = "personalities"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(String(255), nullable=False)

    system_prompt = Column(Text, nullable=False)

    voice = Column(String(50), nullable=False)