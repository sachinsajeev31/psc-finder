import json
import sqlite3


DATABASE = "psc_finder.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    return connection


def migrate_posts():

    connection = get_connection()

    cursor = connection.cursor()

    with open(
        "data/posts.json",
        "r",
        encoding="utf-8"
    ) as file:

        posts = json.load(file)

    for post in posts:

        cursor.execute("""
            INSERT OR IGNORE INTO posts
            (
                id,
                name,
                qualification,
                min_age,
                max_age,
                district,
                status,
                description,
                important
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            post["id"],
            post["name"],
            post["qualification"],
            post["min_age"],
            post["max_age"],
            post["district"],
            post["status"],
            post["description"],
            post["important"]
        ))

    connection.commit()

    connection.close()

    print("Posts migrated successfully!")



def migrate_syllabus():

    connection = get_connection()

    cursor = connection.cursor()

    with open(
        "data/syllabus.json",
        "r",
        encoding="utf-8"
    ) as file:

        syllabuses = json.load(file)

    for syllabus in syllabuses:

        cursor.execute("""
            INSERT OR IGNORE INTO syllabus
            (
                id,
                post,
                description
            )
            VALUES (?, ?, ?)
        """, (
            syllabus["id"],
            syllabus["post"],
            syllabus["description"]
        ))

        for topic in syllabus["topics"]:

            cursor.execute("""
                INSERT INTO syllabus_topics
                (
                    syllabus_id,
                    topic
                )
                VALUES (?, ?)
            """, (
                syllabus["id"],
                topic
            ))

    connection.commit()

    connection.close()

    print("Syllabus migrated successfully!")
def migrate_exams():

    connection = get_connection()

    cursor = connection.cursor()

    with open(
        "data/exams.json",
        "r",
        encoding="utf-8"
    ) as file:

        exams = json.load(file)

    for exam in exams:

        cursor.execute("""
            INSERT OR IGNORE INTO exams
            (
                id,
                post,
                category,
                exam_date,
                status,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            exam["id"],
            exam["post"],
            exam["category"],
            exam["exam_date"],
            exam["status"],
            exam["description"]
        ))

    connection.commit()

    connection.close()

    print("Exams migrated successfully!")
def migrate_questions():

    connection = get_connection()

    cursor = connection.cursor()

    with open(
        "data/questions.json",
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(file)

    for question in questions:

        cursor.execute("""
            INSERT OR IGNORE INTO questions
            (
                id,
                question,
                option1,
                option2,
                option3,
                option4,
                answer,
                subject
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question["id"],
            question["question"],
            question["options"][0],
            question["options"][1],
            question["options"][2],
            question["options"][3],
            question["answer"],
            question["subject"]
        ))

    connection.commit()

    connection.close()

    print("Questions migrated successfully!")
if __name__ == "__main__":
    migrate_posts()
    migrate_syllabus()  
    migrate_exams()  
    migrate_questions()