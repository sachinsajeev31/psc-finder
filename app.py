from flask import Flask, render_template, request
import json
from database import get_db_connection

app = Flask(__name__)


# -----------------------------
# Load PSC post data
# -----------------------------

def load_posts():

    with open("data/posts.json", "r", encoding="utf-8") as file:
        return json.load(file)


# -----------------------------
# Load syllabus data
# -----------------------------

def load_syllabus():

    with open("data/syllabus.json", "r", encoding="utf-8") as file:
        return json.load(file)


# -----------------------------
# Home
# -----------------------------

@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------
# Find Posts
# -----------------------------

@app.route("/posts", methods=["GET", "POST"])
def posts():

    matching_posts = []
    searched = False

    if request.method == "POST":

        searched = True

        qualification = request.form.get("qualification")
        age = int(request.form.get("age"))
        district = request.form.get("district")

        connection = get_db_connection()

        matching_posts = connection.execute("""
            SELECT *
            FROM posts
            WHERE
                (qualification = ? OR qualification = 'Any Degree')
                AND min_age <= ?
                AND max_age >= ?
                AND (district = 'All Kerala' OR district = ?)
        """, (
            qualification,
            age,
            age,
            district
        )).fetchall()

        connection.close()

    return render_template(
        "posts.html",
        matching_posts=matching_posts,
        searched=searched
    )


# -----------------------------
# Post Details
# -----------------------------

@app.route("/post/<int:post_id>")
def post_details(post_id):

    connection = get_db_connection()

    post = connection.execute("""
        SELECT *
        FROM posts
        WHERE id = ?
    """, (post_id,)).fetchone()

    connection.close()

    if post is None:
        return "Post not found", 404

    return render_template(
        "post_details.html",
        post=post
    )


# -----------------------------
# Syllabus
# -----------------------------

@app.route("/syllabus")
def syllabus():

    search = request.args.get("search", "").strip()

    connection = get_db_connection()

    if search:

        syllabuses = connection.execute("""
            SELECT *
            FROM syllabus
            WHERE post LIKE ?
        """, (
            f"%{search}%",
        )).fetchall()

    else:

        syllabuses = connection.execute("""
            SELECT *
            FROM syllabus
        """).fetchall()

    connection.close()

    return render_template(
        "syllabus.html",
        syllabuses=syllabuses,
        search=search
    )


# -----------------------------
# Syllabus Details
# -----------------------------

@app.route("/syllabus/<int:syllabus_id>")
def syllabus_details(syllabus_id):

    connection = get_db_connection()

    syllabus = connection.execute("""
        SELECT *
        FROM syllabus
        WHERE id = ?
    """, (syllabus_id,)).fetchone()

    if syllabus is None:

        connection.close()

        return "Syllabus not found", 404

    topics = connection.execute("""
        SELECT topic
        FROM syllabus_topics
        WHERE syllabus_id = ?
    """, (syllabus_id,)).fetchall()

    connection.close()

    return render_template(
        "syllabus_details.html",
        syllabus=syllabus,
        topics=topics
    )
# -----------------------------
# Exams
# -----------------------------

def load_exams():

    with open("data/exams.json", "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/exams")
def exams():

    selected_category = request.args.get(
        "category",
        ""
    ).strip()

    connection = get_db_connection()

    if selected_category:

        exams = connection.execute("""
            SELECT *
            FROM exams
            WHERE category = ?
            ORDER BY id
        """, (
            selected_category,
        )).fetchall()

    else:

        exams = connection.execute("""
            SELECT *
            FROM exams
            ORDER BY id
        """).fetchall()

    connection.close()

    return render_template(
        "exams.html",
        exams=exams,
        selected_category=selected_category
    )


# -----------------------------
# Exam Details
# -----------------------------

@app.route("/exam/<int:exam_id>")
def exam_details(exam_id):

    connection = get_db_connection()

    exam = connection.execute("""
        SELECT *
        FROM exams
        WHERE id = ?
    """, (exam_id,)).fetchone()

    connection.close()

    if exam is None:
        return "Exam not found", 404

    return render_template(
        "exam_details.html",
        exam=exam
    )
    
# -----------------------------
# Load Questions
# -----------------------------

def load_questions():

    connection = get_db_connection()

    rows = connection.execute("""
        SELECT *
        FROM questions
        ORDER BY id
    """).fetchall()

    connection.close()

    questions = []

    for row in rows:

        questions.append({
            "id": row["id"],
            "question": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ],
            "answer": row["answer"],
            "subject": row["subject"]
        })

    return questions


# -----------------------------
# Mock Tests
# -----------------------------

@app.route("/mock-tests")
def mock_tests():

    return render_template("mock_tests.html")


@app.route("/mock-test", methods=["GET", "POST"])
def mock_test():
    questions = load_questions()

    if request.method == "POST":

        score = 0
        total = len(questions)

        # Subject-wise statistics
        subject_stats = {}

        for question in questions:

            subject = question["subject"]

            if subject not in subject_stats:
                subject_stats[subject] = {
                    "correct": 0,
                    "total": 0
                }

            subject_stats[subject]["total"] += 1

            user_answer = request.form.get(
                f"question_{question['id']}"
            )

            if user_answer is not None:

                if int(user_answer) == question["answer"]:
                    score += 1
                    subject_stats[subject]["correct"] += 1

        # Calculate percentages
        for subject, stats in subject_stats.items():

            stats["percentage"] = round(
                (stats["correct"] / stats["total"]) * 100
            )

        correct = score
        wrong = total - correct

        percentage = round(
            (score / total) * 100
        )

        # Find strongest and weakest subjects
        strongest_subject = max(
            subject_stats,
            key=lambda x: subject_stats[x]["percentage"]
        )

        weakest_subject = min(
            subject_stats,
            key=lambda x: subject_stats[x]["percentage"]
        )

        return render_template(
            "test_result.html",
            score=score,
            total=total,
            correct=correct,
            wrong=wrong,
            percentage=percentage,
            subject_stats=subject_stats,
            strongest_subject=strongest_subject,
            weakest_subject=weakest_subject
        )

    return render_template(
        "mock_test.html",
        questions=questions
    )





# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)