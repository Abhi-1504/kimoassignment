from fastapi import FastAPI
from pydantic import BaseModel
from dbloader import MongoDbConn
from typing import Optional

app = FastAPI()
mongo_db_conn = MongoDbConn()



@app.get("/courses/{sort_by}", description="Endpoint to get all the courses sorted")
async def get_all_courses(sort_by : str, domain: Optional[str] = None):
    return mongo_db_conn.get_all_courses(sort_by, domain)

@app.get("/course_overview", description="Endpoint to get an overiew of a course")
async def get_course_overiew(course_name: str):
    return mongo_db_conn.get_course_overview(course_name)