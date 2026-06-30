# services/database.py
import sqlite3
from config import DATABASE_NAME

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        grade TEXT,
        age INTEGER,
        favorite_subject TEXT,
        weak_subject TEXT,
        learning_style TEXT,
        language TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        student_grade TEXT,
        student_age INTEGER,
        activity_type TEXT,
        topic TEXT,
        score INTEGER,
        subject TEXT,
        strand TEXT,
        sub_strand TEXT,
        learning_outcome TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_student(student):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO students (name, grade, age, favorite_subject, weak_subject, learning_style, language)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student["name"], student["grade"], student["age"], student["favorite_subject"], student["weak_subject"], student["learning_style"], student["language"]))
    conn.commit()
    conn.close()

def save_activity(student_name, student_grade, student_age, activity_type, topic, score=0, subject="General", topics="General", sub_topic="General", learning_outcome="General"):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO progress (student_name, student_grade, student_age, activity_type, topic, score, subject, strand, sub_strand, learning_outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_name, student_grade, int(student_age), activity_type, topic, score, subject, topics, sub_topic, learning_outcome))
    conn.commit()
    conn.close()

def get_student_stats(student_name, student_grade, student_age):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT COUNT(*) FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'question'
    """, (student_name, student_grade, int(student_age)))
    questions = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT COUNT(*) FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
    """, (student_name, student_grade, int(student_age)))
    quizzes = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT AVG(score) FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
    """, (student_name, student_grade, int(student_age)))
    avg_score = cursor.fetchone()[0]
    avg_score = round(avg_score) if avg_score else 0
    
    conn.close()
    return {"questions": questions, "quizzes": quizzes, "average_score": avg_score}

def get_student_quiz_history(student_name, student_grade, student_age):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT score FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
    ORDER BY created_at ASC
    """, (student_name, student_grade, int(student_age)))
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    return scores

def get_next_difficulty(student_name, student_grade, student_age, topic):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT score FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND topic = ? AND activity_type = 'quiz_score'
    ORDER BY created_at DESC LIMIT 3
    """, (student_name, student_grade, int(student_age), topic))
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    if not scores:
        return "Medium"
    avg = sum(scores) / len(scores)
    if avg >= 80:
        return "Hard"
    elif avg < 50:
        return "Easy"
    return "Medium"

def get_student_learning_analysis(student_name, student_grade, student_age):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT topic, AVG(score) FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ? AND activity_type = 'quiz_score'
    GROUP BY topic
    """, (student_name, student_grade, int(student_age)))
    topic_averages = cursor.fetchall()
    conn.close()
    
    weak_topics = [topic for topic, avg in topic_averages if avg < 70]
    strong_topics = [topic for topic, avg in topic_averages if avg >= 80]
    all_scores = [avg for topic, avg in topic_averages]
    overall_avg = sum(all_scores) / len(all_scores) if all_scores else 0
    
    if overall_avg < 50:
        current_level = "Easy"
    elif overall_avg < 80:
        current_level = "Medium"
    else:
        current_level = "Hard"
        
    return {"weak_topics": weak_topics, "strong_topics": strong_topics, "current_level": current_level}

def get_chat_history(student_name: str, grade: str, age: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT activity_type, topic FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ?
    AND (activity_type = 'student' OR activity_type = 'assistant')
    ORDER BY id ASC
    """, (student_name, grade, int(age)))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": "user" if r[0] == "student" else "assistant", "content": r[1]} for r in rows]

def save_chat_message(student_name: str, grade: str, age: int, role: str, message: str):
    activity = "student" if role in ["user", "student"] else "assistant"
    save_activity(
        student_name=student_name, student_grade=grade, student_age=int(age),
        activity_type=activity, topic=message, score=0
    )

def clear_student_chat_history(student_name: str, grade: str, age: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM progress
    WHERE student_name = ? AND student_grade = ? AND student_age = ?
    """, (student_name, grade, int(age)))
    conn.commit()
    conn.close()