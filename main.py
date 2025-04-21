from fastapi import FastAPI, Query, Depends
from schemas import StoryRequest
from sqlalchemy.orm import Session
from models import Story
from database import engine, Base, get_db
from utils import generate_childhood, generate_historical_conflict, generate_historical_context, generate_profession


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to medieval stories generator!"}


@app.post("/generate-story")
def generate_story(
    request: StoryRequest,
    db: Session = Depends(get_db)
):
    period_context = generate_historical_context()
    base_story = f"You were born into a {request.social_class.value} family in {request.region} {period_context}. "
    base_story += generate_childhood(request.social_class)
    base_story += " " + generate_profession(request.social_class)

    if request.include_conflict:
        base_story += " " + generate_historical_conflict(request.social_class)

    db_story = Story(
        social_class=request.social_class.value,
        region=request.region,
        story_text=base_story
    )

    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    return {
        "id": db_story.id,
        "story": base_story,
        "created_at": db_story.created_at
    }


@app.get("/stories/")
def read_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    stories = db.query(Story).offset(skip).limit(limit).all()
    total = db.query(Story).count()

    return {
        "items": stories,
        "total": total,
        "skip": skip,
        "limit": limit
    }
