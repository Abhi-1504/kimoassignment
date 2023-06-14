import pymongo
from configparser import ConfigParser
from typing import List, Dict, Optional, Tuple, Union

config = ConfigParser()
config.read("config.conf")
HOST = config.get("DATABASE", "Host")
Port = int(config.get("DATABASE", "Port"))


class MongoDbConn:
    def __init__(self):
        self.client = pymongo.MongoClient(HOST, Port)
        self.database = self.client["kimodb"]
        self.courses_collection = self.database["courses"]
        self.chapters_collection = self.database["chapters"]

    def get_course_doc(self, query: Union[Dict, Tuple]) -> Dict:
        return self.courses_collection.find_one(
            *query if isinstance(query, tuple) else query
        )

    def get_chapter_doc(self, query: Union[Dict, Tuple]) -> Dict:
        if isinstance(query, tuple):
            return self.chapters_collection.find_one(
            *query)
        else:
            return self.chapters_collection.find_one(
            query)
    
    def update_course_ratings(self, course_doc : Dict, chapters_ratings: List[Dict]) -> Dict:
        
        overall_rating = sum([1 if user_rating["rated"].lower() == "positive" else -1 if user_rating["rated"].lower() == "negative" else 0 for user_rating in chapters_ratings])
        self.courses_collection.update_one({"_id": course_doc["_id"]}, {"$set" : {"ratings" : overall_rating} })

    def get_all_courses(self, sort_by: str, domain: Optional[str] = None) -> List[Dict]:

        query = {"domain": domain} if domain else {}

        all_courses_docs = self.courses_collection.find(query, {"_id": False}).sort(
                sort_by , pymongo.ASCENDING if sort_by == "name" else pymongo.DESCENDING)
            

        all_courses = []
        for course_doc in all_courses_docs:
            course_doc["date"] = course_doc["date"].strftime("%Y-%m-%d %H:%M:%S")
            course_chapters_docs = self.chapters_collection.find(
                {"_id": {"$in": course_doc["chapter_ids"]}},
                {"_id": False, "course_id": False},
            )
            course_doc["chapters"] = list(course_chapters_docs)
            course_doc.pop("chapter_ids")
            all_courses.append(course_doc)

        return all_courses

    def get_course_overview(self, course_name: str) -> Dict:

        query = {"name": course_name}, {"_id": False, "chapter_ids": False}
        course_doc = self.get_course_doc(query)
        course_doc["date"] = course_doc["date"].strftime("%Y-%m-%d %H:%M:%S")
        return course_doc

    def get_chapter_information(self, chapter_name: str) -> Dict:

        query = {"name": chapter_name}, {"_id": False}
        chapter_doc = self.get_chapter_doc(query)
        query = {"_id": chapter_doc["course_id"]}, {"name": True}
        course_name = self.get_course_doc(query)["name"]
        chapter_doc.pop("course_id")
        chapter_doc["course_name"] = course_name

        return chapter_doc

    def post_chapter_rating(self, user_id: str, chapter_name: str, rating: str) -> Dict:

        query = {"name": chapter_name}
        chapter_doc = self.get_chapter_doc(query)
        query = {"_id": chapter_doc["course_id"]}, {"_id" : True}
        course_doc = self.get_course_doc(query)

        for user_rating in chapter_doc["ratings"]:
            if user_id == user_rating["user_id"]:
                user_rating["rated"] = rating
                break
        else:
            chapter_doc['ratings'].append({"user_id" : user_id, "rated" : rating})

        self.chapters_collection.update_one({"_id" : chapter_doc["_id"]}, {"$set": {"ratings" : chapter_doc["ratings"]}})

        self.update_course_ratings(course_doc, chapter_doc["ratings"])




        

        



