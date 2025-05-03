#!/bin/bash

# Configuration
BACKEND_URL="http://localhost:8000"
MIN_EVENTS=10
LOG_FILE="server.log"
PORT=8000
DB_FILE="events.db"

# Function to check if a command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "❌ Error: $1 failed"
        exit 1
    fi
}

# Function to check if port is in use
check_port() {
    if lsof -i :$PORT > /dev/null 2>&1; then
        echo "Port $PORT is already in use. Killing existing process..."
        lsof -ti :$PORT | xargs kill -9
        sleep 2
    fi
}

# Function to wait for server to be ready
wait_for_server() {
    echo "⏳ Waiting for server to start..."
    for i in {1..30}; do
        if curl -s "$BACKEND_URL/events/" > /dev/null; then
            echo "✅ Server is ready!"
            return 0
        fi
        sleep 1
    done
    echo "❌ Server failed to start"
    return 1
}

# Clean up old database file
echo "🧹 Cleaning up old database..."
rm -f "$DB_FILE"

# Check and free up port if needed
check_port

# Start the backend server in the background
echo "🚀 Starting backend server..."
python3 -m uvicorn backend.app.main:app --reload --port $PORT > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Wait for server to be ready
wait_for_server
check_status "Server startup"

# Add a delay to ensure database is initialized
echo "⏳ Waiting for database initialization..."
sleep 5

# Purge the database
echo "🗑️ Purging database..."
PURGE_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/purge-db")
if [[ $PURGE_RESPONSE == *"error"* ]]; then
    echo "❌ Error purging database: $PURGE_RESPONSE"
    kill $SERVER_PID
    exit 1
fi
echo "✅ Database purged successfully"

# Trigger the scraper
echo "🔄 Triggering scraper..."
SCRAPER_RESPONSE=$(curl -s -X POST "${BACKEND_URL}/trigger-scraper")
if [[ $SCRAPER_RESPONSE == *"error"* ]]; then
    echo "❌ Error triggering scraper: $SCRAPER_RESPONSE"
    kill $SERVER_PID
    exit 1
fi
echo "✅ Scraper triggered successfully"

# Wait for scraping to complete
echo "⏳ Waiting for scraping to complete..."
sleep 5

# Get events and check count
echo "📊 Checking event count..."
EVENT_COUNT=$(curl -s "http://localhost:8000/events/" | jq 'length')
echo "EVENT_COUNT: $EVENT_COUNT"
check_status "Event count check"

echo "Found $EVENT_COUNT events"

# Check if we have enough events
if [ "$EVENT_COUNT" -ge "$MIN_EVENTS" ]; then
    echo "✅ Success: Found $EVENT_COUNT events (minimum required: $MIN_EVENTS)"
else
    echo "❌ Error: Found only $EVENT_COUNT events (minimum required: $MIN_EVENTS)"
    kill $SERVER_PID
    exit 1
fi

# Clean up
echo "🧹 Cleaning up..."
kill $SERVER_PID
sleep 2  # Give the server time to shut down
if ps -p $SERVER_PID > /dev/null; then
    echo "Server still running, forcing kill..."
    kill -9 $SERVER_PID
fi
rm -f "$LOG_FILE"

echo "✨ Test completed successfully!" 