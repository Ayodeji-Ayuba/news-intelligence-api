from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.models import Story
from schemas.schemas import StoryResponse
from utils.database import get_db
from google import genai
import os

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("/", response_model=list[StoryResponse])
def get_stories(db: Session = Depends(get_db)):
    stories = db.query(Story).all()
    return stories


@router.get("/{story_id}", response_model=StoryResponse)
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/{id}/summary")
def get_story_summary(id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prompt = f"Based on this article title, briefly explain in 2-3 sentences what this article is likely about: '{story.title}'"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        summary = response.text
    except Exception as e:
        raise HTTPException(
            status_code=503, detail="AI summary temporarily unavailable. Try again later.")

    return {
        "id": story.id,
        "title": story.title,
        "summary": summary
    }
