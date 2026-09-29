from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils.database import get_db
from scraper.scraper import scrape_stories
from routers.stories import router as stories_router

app = FastAPI(
    title="News Intelligence API",
    description="Scrapes and serves Hacker News stories",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(stories_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scrape")
def scrape_stories_endpoint(db: Session = Depends(get_db)):
    saved, skipped = scrape_stories(db)
    return {"saved": saved, "skipped": skipped}
