from pydantic import BaseModel

class ChapterRatingRequest(BaseModel):
    user_id : str
    chapter_name: str
    rating : str