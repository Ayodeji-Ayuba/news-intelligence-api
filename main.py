from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils.database import get_db
from scraper.scraper import scrape_stories
from routers.stories import router as stories_router
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from models.models import SessionLocal

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

scheduler = BackgroundScheduler()


def scheduled_scrape():
    db = SessionLocal()
    try:
        saved, skipped = scrape_stories(db)
        print(f"Scheduled scrape: saved {saved}, skipped {skipped}")
    finally:
        db.close()


@app.on_event("startup")
def startup():
    scheduler.add_job(
        func=scheduled_scrape,
        trigger=IntervalTrigger(hours=6),
        id="scrape_job",
        name="Scrape Stories"
    )
    scheduler.start()


@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scrape")
def scrape_stories_endpoint(db: Session = Depends(get_db)):
    saved, skipped = scrape_stories(db)
    return {"saved": saved, "skipped": skipped}
