import sqlite3


DATABASE = "psc_finder.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def create_tables():

    connection = get_db_connection()

    cursor = connection.cursor()

    # Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            qualification TEXT NOT NULL,
            min_age INTEGER,
            max_age INTEGER,
            district TEXT,
            status TEXT,
            description TEXT,
            important TEXT
        )
    """)

    # Syllabus table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syllabus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post TEXT NOT NULL,
            description TEXT
        )
    """)
        # Syllabus topics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS syllabus_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syllabus_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            FOREIGN KEY (syllabus_id) REFERENCES syllabus(id)
        )
    """)

    # Exams table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post TEXT NOT NULL,
            category TEXT,
            exam_date TEXT,
            status TEXT,
            description TEXT
        )
    """)

    # Questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer INTEGER,
            subject TEXT
        )
    """)

    connection.commit()

    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database created successfully!")