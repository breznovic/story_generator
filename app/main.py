from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
import random
from enum import Enum
from sqlalchemy.orm import Session
from .models import Story
from .database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


class SocialClass(str, Enum):
    PEASANT = "peasant"
    KNIGHT = "knight"
    MERCHANT = "merchant"
    NOBLE = "noble"
    CLERIC = "cleric"


class StoryRequest(BaseModel):
    social_class: SocialClass
    region: str
    include_conflict: bool = True


@app.get("/")
def read_root():
    return {"message": "Welcome to medieval stories generator!"}


def generate_childhood(social_class: SocialClass) -> str:
    options = [
        "From childhood you helped your {parent}.",
        "You spent your days {activity}.",
        "Your early years were spent {doing}."
    ]

    activities = {
        SocialClass.PEASANT: {
            "parent": ["father in the fields", "mother with spinning wool", "uncle in the mill"],
            "activity": ["herding sheep", "working in the village", "gathering firewood"],
            "doing": ["learning peasant crafts", "serving the local lord", "surviving hardships"]
        },
        SocialClass.KNIGHT: {
            "parent": ["father in arms practice", "mother in the manor", "knightly mentor"],
            "activity": ["training with wooden swords", "studying chivalry", "caring for horses"],
            "doing": ["serving as a page", "learning courtly manners", "attending tournaments"]
        },
        SocialClass.MERCHANT: {
            "parent": ["father in the marketplace", "mother keeping accounts", "uncle on trading voyages"],
            "activity": ["learning numbers", "observing deals", "packing goods"],
            "doing": ["studying foreign tongues", "traveling with caravans", "haggling prices"]
        },
        SocialClass.NOBLE: {
            "parent": ["father at court", "mother hosting feasts", "governess"],
            "activity": ["learning heraldry", "practicing music", "riding horses"],
            "doing": ["studying politics", "managing estates", "arranging marriages"]
        },
        SocialClass.CLERIC: {
            "parent": ["priest father", "abbess mother", "monastic tutor"],
            "activity": ["copying manuscripts", "praying in chapel", "tending herb garden"],
            "doing": ["studying scripture", "serving the poor", "learning Latin"]
        }
    }

    template = random.choice(options)
    return template.format(
        parent=random.choice(activities[social_class]["parent"]),
        activity=random.choice(activities[social_class]["activity"]),
        doing=random.choice(activities[social_class]["doing"])
    )


def generate_profession(social_class: SocialClass) -> str:
    professions = {
        SocialClass.PEASANT: [
            "You became a skilled farmer.",
            "You were bound to the land as a serf.",
            "You mastered the craft of your village."
        ],
        SocialClass.KNIGHT: [
            "You were knighted after proving your valor.",
            "You became a landless knight errant.",
            "You inherited your father's estates."
        ],
        SocialClass.MERCHANT: [
            "You established trade routes across the sea.",
            "You became a guild master.",
            "You specialized in rare spices and silks."
        ],
        SocialClass.NOBLE: [
            "You inherited your family's titles.",
            "You became a trusted advisor to the crown.",
            "You married into a powerful dynasty."
        ],
        SocialClass.CLERIC: [
            "You took holy vows and joined the clergy.",
            "You became a learned scholar of theology.",
            "You were appointed to an important abbey."
        ]
    }
    return random.choice(professions[social_class])


def generate_historical_context() -> str:
    contexts = [
        "during the Migration Period",
        "in the time of Charlemagne",
        "after the fall of Rome",
        "during the Crusades",
        "in the era of feudal lords",
        "when castles dotted the landscape",
        "during the Hundred Years' War",
        "as the Black Death spread",
        "when kingdoms were consolidating power",
    ]
    return random.choice(contexts)


def generate_historical_conflict(social_class: SocialClass) -> str:
    conflicts = {
        SocialClass.PEASANT: [
            "Your village was caught between feuding lords",
            "A poor harvest led to famine and unrest",
            "Tax collectors demanded more than you could give",
            "Your family was forced to flee from raiders",
            "The lord increased your corvée obligations",
            "Your crops were trampled by a lord's hunting party",
            "You participated in a peasant revolt against unjust taxes",
            "Your son was taken as a serf to another manor",
            "A local monastery claimed your best fields",
            "Wolves decimated your livestock during a harsh winter"
        ],
        SocialClass.KNIGHT: [
            "You fought in a bloody battle for your liege",
            "A siege tested your courage and skills",
            "You uncovered a plot against your lord",
            "Your castle was attacked by rival nobles",
            "You were taken prisoner and had to pay ransom",
            "You led troops to put down a peasant rebellion",
            "Your liege demanded you join an unpopular war",
            "Your lands were ravaged by mercenary companies",
            "You participated in a tournament that turned deadly",
            "Your squire betrayed you to a rival house"
        ],
        SocialClass.MERCHANT: [
            "Your trade caravan was ambushed by bandits",
            "A rival guild undercut your prices",
            "Your goods were confiscated by corrupt officials",
            "Pirates sank your valuable cargo ship",
            "You were accused of violating trade monopolies",
            "Your debtors refused to pay what they owed",
            "A fire destroyed your warehouse and inventory",
            "You were caught between warring city-states",
            "Your partner fled with the company's funds",
            "The church condemned your business as usury"
        ],
        SocialClass.NOBLE: [
            "Your family was caught in a dynastic war",
            "Your heir married against your wishes",
            "The king demanded your lands as payment for debt",
            "Your vassals rebelled against your rule",
            "A rival family spread vicious rumors about you",
            "Your castle was struck by a devastating plague",
            "You were forced to take sides in a papal schism",
            "Your daughter was abducted by a neighboring lord",
            "Your hunting accident left you unable to rule",
            "Your family's ancient privileges were revoked"
        ],
        SocialClass.CLERIC: [
            "Your monastery was sacked by invaders",
            "You were accused of heresy by rivals",
            "Your bishop demanded impossible tithes",
            "Plague decimated your monastic community",
            "You discovered corruption in the church hierarchy",
            "Your library was destroyed in a fire",
            "Secular lords seized your order's lands",
            "You were caught between papal and royal authority",
            "Your vow of poverty clashed with church politics",
            "A rival order falsely accused you of witchcraft"
        ]
    }
    return random.choice(conflicts[social_class])


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
