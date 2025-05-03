from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from ..core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    venue = Column(String, index=True)
    date = Column(DateTime)
    ticket_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 