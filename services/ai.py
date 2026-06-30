import os
import json
import random
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load keys from local .env file if it exists
load_dotenv()

# 2. Unified fallback: check system environment variables first, then fallback to Streamlit secrets
api_key = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

# 3. Initialize unified OpenRouter gateway client safely
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key if api_key else "MOCK_KEY"
)

def ask_mwalimu(question, student, messages, adaptive_context=""):
    """Dispatches prompts to a specific high-quality free model on OpenRouter."""
    
    # Build conversation history context string safely
    history = ""
    for msg in messages:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            role = str(msg["role"]).lower()
            content = msg["content"]
            if role in ["student", "user"]:
                history += f"Student: {content}\n"
            elif role in ["assistant", "mwalimu"]:
                history += f"Mwalimu AI: {content}\n"

    prompt = f"""
You are Mwalimu AI App, a friendly Kenyan teacher.

=== STUDENT PROFILE ===
Name: {student.get("name", "Student")}
Grade: {student.get("grade", "N/A")}
Age: {student.get("age", "N/A")}
Favorite Subject: {student.get("favorite_subject", "N/A")}
Weak Subject: {student.get("weak_subject", "N/A")}
Learning Style: {student.get("learning_style", "General")}
Language: {student.get("language", "English")}

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Strand: {student.get("strand", "General")}
Sub-strand: {student.get("sub_strand", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

=== ADAPTIVE LEARNING ANALYSIS ===
{adaptive_context}

=== PREVIOUS CONVERSATION ===
{history}

=== CURRENT QUESTION ===
Student: {question}

=== TEACHING RULES ===
- Explain according to the student's age and grade.
- Use the student's preferred language (English, Kiswahili, or Sheng).
- Adapt directly to the student's learning style.
- Be encouraging and patient.
- Give examples and short practice questions.
- Remember previous parts of the conversation.
- ADAPTIVE RULE: If the question is about a topic listed in their 'Weak Topics', break it down into much simpler foundational steps.
- ADAPTIVE RULE: If their 'Current Level' is 'Hard', challenge them with an analytical thinking follow-up question.

Give a clear educational response.
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e).lower()
        print(f"OpenRouter API Error: {e}")
        if "429" in error_msg or "rate" in error_msg:
            return "Pole! 🇰🇪 My classroom has a small queue. Please wait 5 seconds and click ask again!"
        return f"Mwalimu encountered an error while thinking: {e}. Please try again!"

def generate_quiz(topic, student, difficulty="Easy"):
    """Generates structured JSON quiz variations based on adaptive parameters."""
    difficulty_rules = {
        "Easy": "Use very simple language. Focus on one core concept per question. No trick questions.",
        "Medium": "Slightly more challenging. Require two-step thinking. Use localized practical examples.",
        "Hard": "Incorporate complex application questions, critical thinking scenarios, and higher-order reasoning."
    }
    
    prompt = f"""
You are Mwalimu AI, a friendly Kenyan teacher personalization model.

Generate a multiple-choice quiz about '{topic}' for a student in {student.get('grade')} ({student.get('age')} years old).

CRITICAL STRUCTURE RULE: You MUST generate exactly 5 distinct multiple-choice questions. 

Target Difficulty Level: {difficulty}
Difficulty Context Rules: {difficulty_rules.get(difficulty, "")}
Preferred Learning Style: {student.get('learning_style', 'General')}
Preferred Delivery Language: {student.get('language', 'English')}

CBC Context Info:
Subject: {student.get('subject')} | Topic: {student.get('topic')} | Target Learning Outcome: {student.get('learning_outcome')}

Return your response strictly as a valid JSON array containing EXACTLY 5 objects structured exactly like this layout format:
[
  {{
    "question": "First Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The exact correct option string matching one of the options"
  }},
  ... up to 5 elements total
]
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App Quiz",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        quiz_text = response.choices[0].message.content
        if quiz_text is None:
            print("No content returned from model")
            return []
            
        quiz_text = quiz_text.replace("```json", "").replace("```", "").strip()
        try:
            quiz_data = json.loads(quiz_text)
            for question in quiz_data:
                if "options" in question and isinstance(question["options"], list):
                    random.shuffle(question["options"])
            return quiz_data
        except json.JSONDecodeError:
            print("Invalid JSON returned by Model:")
            print(quiz_text)
            return []
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return []

def generate_study_plan(student, stats):
    """Generates a daily personalized study plan based on student profile and quiz history metrics."""
    prompt = f"""
You are Mwalimu AI, an intelligent Kenyan teacher.
Create a personalized DAILY STUDY PLAN.

Student Profile
Name: {student.get("name", "Student")}
Grade: {student.get("grade", "N/A")}
Age: {student.get("age", "N/A")}
Favorite Subject: {student.get("favorite_subject", "N/A")}
Weak Subject: {student.get("weak_subject", "N/A")}
Learning Style: {student.get("learning_style", "General")}
Preferred Language: {student.get("language", "English")}

Active CBC Learning Stream:
Subject Focus: {student.get("subject", "General")} &bull; Strand: {student.get("strand", "General")}

Student Statistics
Questions Asked: {stats.get("questions", 0)}
Quizzes Taken: {stats.get("quizzes", 0)}
Average Score: {stats.get("average_score", 0)}%

Requirements:
Create a highly structured study plan for today. Include:
1. Study Goal (focused on improving their weak subject while keeping them engaged with their favorite subject)
2. Subjects to study
3. Specific Topics
4. Time allocation (e.g., 08:00-08:20)
5. Practical practice activities aligned with their preferred learning style ({student.get("learning_style", "General")})
6. Revision items
7. A dynamic custom Quiz recommendation
8. A warm, motivational message using encouraging Kenyan teacher phrasing (e.g., "Kazi safi", "Keep pushing").

CRITICAL INSTRUCTIONS:
- Write the entire plan in plain, natural English (or Kiswahili where appropriate for a Kenyan teacher).
- NEVER use "Lorem ipsum", placeholder words, or dummy text.
- NEVER include bracketed source numbers or tokens. All content must be completely real and readable.
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI Study Plan",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter Study Plan Error: {e}")
        return f"Mwalimu encountered an issue preparing your roadmap: {e}. Please click generate again!"

def generate_flashcards(topic, student):
    """Generates structured flashcards using OpenRouter based on a topic and the student's background profile."""
    prompt = f"""
You are Mwalimu AI.
Student Profile
Name: {student.get("name")}
Grade: {student.get("grade")}
Age: {student.get("age")}
Learning Style: {student.get("learning_style")}
Language: {student.get("language")}

Create exactly 10 revision flashcards about: {topic}
Return ONLY valid JSON.

Format:
[
  {{
    "question": "...",
    "answer": "..."
  }}
]

Rules:
- Grade appropriate
- Simple language
- No markdown wrappers around json array
- No explanations
- No extra text
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI App Flashcards",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        flash_text = response.choices[0].message.content
        if flash_text is None:
            print("No content returned from model")
            return []
            
        flash_text = flash_text.replace("```json", "").replace("```", "").strip()
        return json.loads(flash_text)
    except json.JSONDecodeError:
        print("Invalid JSON returned by Model.")
        return [
            {"question": f"What is the core concept of {topic}?", "answer": "Mwalimu's notes got slightly jumbled. Please click generate again!"}
        ]
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return [
            {"question": f"What is the core concept of {topic}?", "answer": "Please try generating your deck again."}
        ]

def generate_lesson(topic, student):
    """Generates a structured, pedagogical lesson plan tailored to a student's grade level, learning style, and language preferences using Kenyan contextual references."""
    prompt = f"""
You are Mwalimu AI, an inspiring, friendly, and expert Kenyan school teacher.
Instead of answering a single query, your goal is to generate a comprehensive, structured, and engaging lesson plan for a student.

STUDENT PROFILE:
- Name: {student.get('name', 'Student')}
- Grade: {student.get('grade', 'General')}
- Age: {student.get('age', '10')}
- Learning Style: {student.get('learning_style', 'Interactive')}
- Preferred Language: {student.get('language', 'English')}

LESSON TARGET:
- Topic: {topic}
- Subject Domain: {student.get('subject')} | Strand Focus: {student.get('strand')} | Target Outcome: {student.get('learning_outcome')}

Please construct the lesson using clean Markdown headers. The lesson MUST include the following 9 numbered sections in order:
1. Lesson Title
- Create an exciting and clear title incorporating the topic.
2. Learning Objectives
- State 3 or 4 clear bullet points outlining what the student will be able to do after completing this lesson.
3. Introduction
- Hook the student's interest using a friendly greeting (e.g., using "Mambo!", "Habari!") and relate the topic to everyday life.
4. Main Explanation
- Breakdown the core concepts clearly. Use simple language appropriate for a {student.get('grade')} student.
- Adapt explicitly to a {student.get('learning_style')} learning style.
5. Real-life Kenyan Examples
- Ground the concept with relatable Kenyan contextual examples (e.g., matatus, market scenarios, local food like ugali/sukuma wiki, running tracking).
6. Worked Examples
- Provide step-by-step solutions to 1 or 2 practical problems or case scenarios illustrating the concept.
7. Practice Questions
- Provide 3 progressive questions matching the difficulty of the lesson to encourage active recall and critical thinking. Do not provide the answers immediately.
8. Summary & Fun Fact
- Bullet points summarizing the main takeaways of the lesson, followed by an interesting, mind-blowing fun fact relating to the topic.
9. Homework
- Create an engaging practical activity or mini-assignment that the student can perform at home or around the house to observe the concept in action.

STRICT GUIDELINES:
- Always match the vocabulary to {student.get('grade')} expectations.
- Write primarily in the preferred language: {student.get('language')}.
- Do not append any meta-commentary, safety labels ("User Safety: safe"), or extra prompt diagnostics. Output only the complete lesson content.
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI Lesson Plan Engine",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter Lesson Generation Error: {e}")
        return f"Mwalimu encountered an issue preparing your lesson roadmap: {e}. Please click generate again!"