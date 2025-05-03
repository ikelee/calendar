from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from .core.database import get_db
from .models.event import Event
from .scrapers.run_scrapers import run_scrapers
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class EventResponse(BaseModel):
    id: int
    event_id: str
    title: str
    description: Optional[str]
    venue: str
    date: datetime
    ticket_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

@app.get("/events/", response_model=List[EventResponse])
def get_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    events = db.query(Event).offset(skip).limit(limit).all()
    return events

@app.post("/trigger-scraper")
def trigger_scraper():
    """Trigger the scraper to fetch new events."""
    try:
        events = run_scrapers()
        return {"status": "success", "events_retrieved": len(events)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/purge-db")
async def purge_database(db: Session = Depends(get_db)):
    """Purge all events from the database (for testing only)."""
    try:
        # Delete all events
        num_deleted = db.query(Event).delete()
        db.commit()
        return {"message": f"Successfully deleted {num_deleted} events"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 