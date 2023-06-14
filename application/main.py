from fastapi import FastAPI
from application.model_classes import ChapterRatingRequest
from application.db_loader import MongoDbConn
from typing import Optional

# Creating application for API endpoint routes
app = FastAPI()
mongo_db_conn = MongoDbConn()


@app.get(
    "/courses/{sort_by}",
    description="Endpoint to get all the courses sorted by either name, date or ratings",
)
async def get_all_courses(sort_by: str, domain: Optional[str] = None):
    return mongo_db_conn.get_all_courses(sort_by, domain)


@app.get("/course_overview", description="Endpoint to get an overiew of a course")
async def get_course_overiew(course_name: str):
    return mongo_db_conn.get_course_overview(course_name)


@app.get("/chapter_overview", description="Endpoint to get a chapter overiew")
async def get_chapter_overview(chapter_name: str):
    return mongo_db_conn.get_chapter_information(chapter_name)


@app.post("/chapter_rating", description="Endpoint for rating a chapter")
async def rate_chapter(rating_request: ChapterRatingRequest):
    return rating_request
    return mongo_db_conn.post_chapter_rating(
        rating_request.user_id, rating_request.chapter_name, rating_request.rating
    )
