# Chatbot Backend with FastAPI and MongoDB

This project provides a backend for a chatbot application, using FastAPI and MongoDB.

## Folder Structure

- `app/main.py`: Entry point for the FastAPI app
- `app/models`: Defines Pydantic models for data validation
- `app/database`: MongoDB connection setup
- `app/routes`: CRUD routes for managing conversations

## Getting Started

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

3. Access the API documentation at `http://127.0.0.1:8000/docs`.
