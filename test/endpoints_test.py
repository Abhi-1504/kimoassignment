import sys

sys.path.append("../")

from fastapi.testclient import TestClient
from application.main import app


client = TestClient(app)


def test_courses():
    response = client.get("/courses/name")
    assert response.status_code == 200
    course_list = response.json()
    expected_courses_name = [
        "Computer Vision Course",
        "Highlights of Calculus",
        "Introduction to Deep Learning",
        "Introduction to Programming",
    ]
    expected_courses_date = [
        "Introduction to Programming",
        "Introduction to Deep Learning",
        "Highlights of Calculus",
        "Computer Vision Course",
    ]
    course_list_from_response = []
    for doc in course_list:
        print(type(doc), doc["name"])
        course_list_from_response.append(doc["name"])
    for i in range(4):
        assert expected_courses_name[i] == course_list_from_response[i]

    response = client.get("/courses/date")
    assert response.status_code == 200
    course_list = response.json()
    course_list_from_response = []
    for doc in course_list:
        print(type(doc), doc["name"])
        course_list_from_response.append(doc["name"])
    for i in range(4):
        assert expected_courses_date[i] == course_list_from_response[i]


def test_course_overview():
    response = client.get("/course_overview?course_name=Highlights of Calculus")
    assert response.status_code == 200
    course_overview = response.json()
    assert (
        course_overview["description"]
        == "Highlights of Calculus is a series of short videos that introduces the basic ideas of calculus — how it works and why it is important. The intended audience is high school students, college students, or anyone who might need help understanding the subject.\nIn addition to the videos, there are summary slides and practice problems complete with an audio narration by Professor Strang. You can find these resources to the right of each video."
    )


def test_chapter_info():
    response = client.get(
        "/chapter_overview?chapter_name=Convolutional Neural Networks"
    )
    assert response.status_code == 200
    course_overview = response.json()
    assert course_overview["text"] == "Computer Vision Course"


def test_rating():
    rating = {
        "user_id": "kimo",
        "rating": "positive",
        "chapter_name": "Convolutional Neural Networks",
    }

    response = client.post("/chapter_rating", json=rating)
    print(response.json())
    assert response.json()["status"] == "completed"
