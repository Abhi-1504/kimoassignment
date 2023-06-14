import pymongo
from configparser import ConfigParser
from typing import List, Dict, Optional, Tuple, Union, Iterator

config = ConfigParser()


class MongoDbConn:
    """Class to handle all MongoDb related operations"""

    def __init__(self):
        # Loading all the required objects to connect and operate on momgodb collections
        self.client = pymongo.MongoClient("localhost", 27017)
        self.database = self.client["kimodb"]
        self.courses_collection = self.database["courses"]
        self.chapters_collection = self.database["chapters"]

    def get_course_doc(self, query: Union[Dict, Tuple]) -> Dict:
        """Gets a course document based on the query
        Param(s):
            query (Dict|Tuple) : filter query
        Return(s):
            course_document (Dict) : Single course document based on filter query
        """
        return self.courses_collection.find_one(
            *query if isinstance(query, tuple) else query
        )

    def get_chapter_doc(self, query: Union[Dict, Tuple]) -> Dict:
        """Gets a chapter document based on the query
        Param(s):
            query (Dict|Tuple) : filter query
        Return(s):
            course_document (Dict) : Single chapter document based on filter query
        """
        if isinstance(query, tuple):
            return self.chapters_collection.find_one(*query)
        else:
            return self.chapters_collection.find_one(query)

    def update_course_ratings(
        self, course_doc: Dict, chapters_ratings: Iterator[Dict]
    ) -> Dict:
        """Updates a course document ratings filed based on it's chapter ratings
        Param(s):
            course_doc (Dict) : Course Document for updating rating
            chapters_ratings (Iterator) : All ratings for all chapters
        Returns(s):
            updatedItem object
        """
        overall_rating = sum(
            [
                1
                if user_rating["rated"].lower() == "positive"
                else -1
                if user_rating["rated"].lower() == "negative"
                else 0
                for chapter_ratings in chapters_ratings
                for user_rating in chapter_ratings["ratings"]
            ]
        )
        return self.courses_collection.update_one(
            {"_id": course_doc["_id"]}, {"$set": {"ratings": overall_rating}}
        )

    def get_all_courses(self, sort_by: str, domain: Optional[str] = None) -> List[Dict]:
        """Gets all courses from database
        Param(s):
            sort_by (str) : field to sort the result by with
            domain (str) : optional domain filter
        Returns(s):
            all_courses (list)
        """
        query = {"domain": domain} if domain else {}

        all_courses_docs = self.courses_collection.find(query, {"_id": False}).sort(
            sort_by, pymongo.ASCENDING if sort_by == "name" else pymongo.DESCENDING
        )

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
        """Gets a course overview from database
        Param(s):
            course_name (str): Name of the Course
        Returns(s):
            course overview (Dict)
        """
        query = {"name": course_name}, {"_id": False, "chapter_ids": False}
        course_doc = self.get_course_doc(query)
        course_doc["date"] = course_doc["date"].strftime("%Y-%m-%d %H:%M:%S")
        return course_doc

    def get_chapter_information(self, chapter_name: str) -> Dict:
        """Gets a chapter overview from database
        Param(s):
            chapter_name (str): Name of the Chapter
        Returns(s):
            chapter overview (Dict)
        """
        query = {"name": chapter_name}, {"_id": False}
        chapter_doc = self.get_chapter_doc(query)
        query = {"_id": chapter_doc["course_id"]}, {"name": True}
        course_name = self.get_course_doc(query)["name"]
        chapter_doc.pop("course_id")
        chapter_doc["course_name"] = course_name

        return chapter_doc

    def post_chapter_rating(self, user_id: str, chapter_name: str, rating: str) -> Dict:
        """Posts ratings for a chapter doc
        Param(s):
            user_id (str): Name of the Chapter
            chapter_name (str): chapter name to be rated
            rating (str): rating (positive or negative)
        Returns(s):
            success or failure message
        """
        query = {"name": chapter_name}
        chapter_doc = self.get_chapter_doc(query)
        query = {"_id": chapter_doc["course_id"]}, {"_id": True}
        course_doc = self.get_course_doc(query)
        for user_rating in chapter_doc["ratings"]:
            if user_id == user_rating["user_id"]:
                user_rating["rated"] = rating
                break
        else:
            chapter_doc["ratings"].append({"user_id": user_id, "rated": rating})

        chapter_result = self.chapters_collection.update_one(
            {"_id": chapter_doc["_id"]}, {"$set": {"ratings": chapter_doc["ratings"]}}
        )
        all_chapters = self.chapters_collection.find({"course_id": course_doc["_id"]})
        course_result = self.update_course_ratings(course_doc, all_chapters)

        if chapter_result.acknowledged and course_result.acknowledged:
            return {"status": "completed"}
        else:
            return {"status": "failed"}
