import pymongo
import json
from datetime import datetime

# Creating client to connect to MongoDB
client =pymongo.MongoClient("localhost", 27017)

# Creating kimodb database
db = client.kimodb

# loading content of courses file
with open("courses.json") as f:
    courses_data = json.load(f)

# Traversing through each course object in courses.json
for course in courses_data:

    # Removing chapters list from course object
    chapters_collection = course.pop("chapters")

    # converting the unix timestamp to date
    course["date"] = datetime.fromtimestamp(course["date"])

    # Adding overall ratings field to the course
    course["ratings"] = 0

    # extracting the unique index for the course inserted
    course_id = db.courses.insert_one(course).inserted_id

    # creating documents for all the chapters for all the courses
    chapters_collection = [{**chapters_document, "course_id": course_id}   for chapters_document in chapters_collection]

    # inserting all the chapters to mongodb collection in bulk
    db.chapters.insert_many(chapters_collection)

    # retriving chapters name and inserted id from collection 
    chapters = db.chapters.find({"course_id" : course_id}, {"name":True})

    # embedding the chapters document data into courses collection's documents
    db.courses.update_one({"_id": course_id}, {"$set": {"chapters" : list(chapters)}})



