from pydantic import BaseModel, ConfigDict
from datetime import datetime


class StoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    source: str
    scraped_at: datetime
