# News Intelligence API

A FastAPI service that scrapes top stories from Hacker News, stores them in PostgreSQL, and generates AI-powered summaries using Google Gemini.

---

## Tech Stack

- **Python 3.14**
- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Playwright** — headless browser for scraping
- **BeautifulSoup4** — HTML parsing
- **Google Gemini** — AI-powered story summaries
- **Pydantic v2** — data validation

---

## Features

- Scrapes top 10 stories from Hacker News on demand
- Stores stories in PostgreSQL with deduplication
- REST API to query stored stories
- AI-generated summaries for any story using Google Gemini
- CORS enabled for frontend integration

---

## API Endpoints

| Method | Endpoint | Description |
|--------|--------------------------|--------------------------------------|
| GET | `/health` | Health check |
| POST | `/scrape` | Scrape and save latest HN stories |
| GET | `/stories/` | Get all stored stories |
| GET | `/stories/{id}` | Get a single story by ID |
| GET | `/stories/{id}/summary` | Get an AI summary of a story |

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Ayodeji-Ayuba/news-intelligence-api.git
cd news-intelligence-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/news_intelligence
GEMINI_API_KEY=your-gemini-api-key-here
```

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

### 5. Create the PostgreSQL database
```bash
psql -U postgres -c "CREATE DATABASE news_intelligence;"
```

### 6. Run the server
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive docs at `http://127.0.0.1:8000/docs`

---

## Example Usage

### Scrape latest stories
```bash
curl -X POST http://127.0.0.1:8000/scrape
```

Response:
```json
{
  "saved": 8,
  "skipped": 2
}
```

### Get all stories
```bash
curl http://127.0.0.1:8000/stories/
```

### Get AI summary
```bash
curl http://127.0.0.1:8000/stories/1/summary
```

Response:
```json
{
  "id": 1,
  "title": "World Labs Is Joining AMD",
  "summary": "This article is likely about a new partnership between World Labs — a spatial intelligence AI startup founded by Fei-Fei Li — and semiconductor giant AMD..."
}
```

---

## Project Structure

```
news-intelligence-api/
├── main.py               # App entry point
├── models/
│   └── models.py         # Database models
├── schemas/
│   └── schemas.py        # Pydantic schemas
├── routers/
│   └── stories.py        # Stories endpoints
├── scraper/
│   └── scraper.py        # Hacker News scraper
├── utils/
│   └── database.py       # DB session dependency
├── .env.example          # Environment variable template
└── requirements.txt
```

---

## Author

**Ayodeji** — [GitHub](https://github.com/Ayodeji-Ayuba)
