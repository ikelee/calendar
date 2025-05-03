from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base

class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    venue = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    url = Column(String) 