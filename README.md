# Event Calendar Scraper

A simple application that scrapes venue websites for events and displays them in a calendar and list view.

## Project Structure

```
.
├── backend/           # Python FastAPI backend
│   ├── main.py       # FastAPI application
│   ├── database.py   # Database models and configuration
│   ├── scraper.py    # Web scraping logic
│   ├── requirements.txt
│   └── Procfile      # Render deployment configuration
└── frontend/         # React frontend (to be added)
```

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Create a .env file:
```bash
echo "DATABASE_URL=sqlite:///./events.db" > .env
```

4. Run the backend:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Deployment on Render

### Backend Deployment

1. Create a new Web Service on Render:
   - Connect your GitHub repository
   - Set the following environment variables:
     - `DATABASE_URL`: Your PostgreSQL database URL (provided by Render)
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. Add a PostgreSQL database:
   - Create a new PostgreSQL database on Render
   - Copy the internal database URL
   - Add it as the `DATABASE_URL` environment variable in your Web Service

### Frontend Deployment (Coming Soon)

The frontend will be deployed as a Static Site on Render.

## API Endpoints

- `GET /events/` - List all events
- `GET /events/{event_id}` - Get a specific event
- `POST /events/` - Create a new event

## Development

For local development, the application uses SQLite. In production, it uses PostgreSQL.

To switch between environments:
1. Local: Use the .env file with SQLite URL
2. Production: Use Render's environment variables with PostgreSQL URL 