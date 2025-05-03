from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Union
from datetime import datetime
import models
import database
from pydantic import BaseModel
from scrapers.run_scrapers import run_scrapers
import logging

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://calendar-frontend.onrender.com",
        "https://calendar-backend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class EventBase(BaseModel):
    title: str
    description: str
    venue: str
    start_time: datetime
    end_time: datetime
    url: str
    image_url: Union[str, None] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# API Endpoints
@app.get("/events/", response_model=List[Event])
def get_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events

@app.post("/events/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(database.get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/")
async def root():
    return {"message": "Calendar API"}

@app.post("/trigger-scraper")
async def trigger_scraper():
    try:
        logging.info("Triggering scraper via API")
        run_scrapers()
        return {"message": "Scraper ran successfully"}
    except Exception as e:
        logging.error(f"Error running scraper: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
