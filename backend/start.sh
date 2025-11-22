#!/bin/bash
# Start Celery worker in the background
celery -A app.worker.celery worker --loglevel=info &

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 10000
