from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    social_class = Column(String, nullable=False)
    region = Column(String, nullable=False)
    story_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
