# 📘 Book AI Platform

This is a full-stack web application that uses AI to work with book data.

It collects books using web scraping, stores them in a backend, and shows them in a simple frontend. Users can view book details, generate summaries, ask questions, and get similar book recommendations.

Even if the AI is not available, the system provides useful results using stored data.

## Features

* View books
* Book details page
* AI summary
* Ask questions
* Similar book recommendations

## Tech Stack

* Backend: Django REST Framework
* Frontend: ReactJS + Tailwind CSS
* Database: SQLite
* AI: OpenAI API (with fallback)
* Scraping: BeautifulSoup


# Document Intelligence Platform for Books

A simple full-stack project that combines Django REST backend, a book scraper, AI question-answering logic, and a React + Tailwind frontend.

## Project Overview

This platform stores book data, scrapes content from `books.toscrape.com`, and answers user questions with simple RAG-like relevance logic.

## Features

- Django REST API for books
- Book model with title, author, description, rating, and URL
- Scraper using `requests` and `BeautifulSoup`
- AI utility module with summarization and fallback question answering
- Lightweight similarity search across book content
- React frontend with book list, details, and question form
- Tailwind CSS styling
- Backend caching for list and question responses

## Tech Stack

- Backend: Python, Django, Django REST Framework, django-cors-headers
- Frontend: React, Tailwind CSS, Axios
- Scraper: requests, BeautifulSoup

## Setup Instructions

### 1. Backend

```powershell
cd c:\Users\anilk\OneDrive\Documents\book-ai-platform\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The backend API runs at `http://127.0.0.1:8000/api/`.

### 2. Frontend

```powershell
cd c:\Users\anilk\OneDrive\Documents\book-ai-platform\frontend
npm install
npm start
```

The frontend runs at `http://localhost:3000`.

## API Endpoints

- `GET /api/books/` — list all books
- `GET /api/books/{id}/` — get one book
- `POST /api/books/` — add a new book
- `POST /api/ask/` — ask a question about books

### Example request body for `POST /api/ask/`

```json
{
  "question": "Which books are good for learning Python?"
}
```

## Scraper

Run the scraper from the backend folder:

```powershell
cd c:\Users\anilk\OneDrive\Documents\book-ai-platform\backend
.\.venv\Scripts\Activate.ps1
python scraper.py
```

It scrapes book titles, ratings, and URLs from `http://books.toscrape.com/` and saves them to the database.

## Sample Questions

- "Which books are best for learning Python?"
- "Show me top rated books."
- "What books have data science in the description?"

## Notes

- If `OPENAI_API_KEY` is set and `openai` is installed, the AI endpoint will attempt a real OpenAI call.
- If OpenAI is unavailable, the app falls back to local book relevance matching.

## Docker Setup

For local development using the existing Docker Compose file:

```powershell
docker-compose up --build
```

For a production-style deployment with Nginx and a static frontend build:

```powershell
docker-compose -f docker-compose.prod.yml up --build
```

Then visit:

- `http://localhost:3000` for the app
- `http://127.0.0.1:8000/api/` for the backend API

The backend migration does not run automatically in production mode, so use this command once before starting the production stack:

```powershell
docker-compose -f docker-compose.prod.yml run backend python manage.py migrate
```

## Future Improvements

- Add real OpenAI integration
- Add authentication
- Add book detail editing
- Add a real search page
## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Book Detail
![Detail](screenshots/detail.png)

### AI Summary
![Summary](screenshots/summary.png)

### Q&A
![Q&A](screenshots/qa.png)