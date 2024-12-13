#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Starting RAG FastAPI service..."
# export PYTHONPATH="/Users/admin/Working/thaibinh-chatbot"

# Start the main application
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
echo "Done RAG FastAPI service..."

# uvicorn main:app --host 127.0.0.1 --port 8000
# echo "127.0.0.1"
