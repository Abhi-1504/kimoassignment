from fastapi import FastAPI
from pydantic import BaseModel
from dbloader import MongoDbConn

app = FastAPI()
mongo_db_conn = MongoDbConn()



@app.get("/courses/{sort_by}", description="Endpoint to get all the courses sorted")
async def get_all_courses(sort_by : str):
    return mongo_db_conn.get_all_courses(sort_by)
