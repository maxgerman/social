#!/bin/bash

# Run migrations
alembic upgrade head

# Run the main application
uvicorn main:app --host 0.0.0.0 --port 8000
