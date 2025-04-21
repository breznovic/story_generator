from pydantic import BaseModel
from utils import SocialClass


class StoryRequest(BaseModel):
    social_class: SocialClass
    region: str
    include_conflict: bool = True
