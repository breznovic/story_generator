from fastapi import FastAPI
from pydantic import BaseModel
import random
from enum import Enum

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


@app.post("/generate-story")
def generate_story(request: StoryRequest):
    story = f"You were born into a {request.social_class.value} family in {request.region}. "
    story += generate_childhood(request.social_class)
    story += " " + generate_profession(request.social_class)
    return {"story": story}
