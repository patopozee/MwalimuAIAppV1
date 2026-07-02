# services/ai.py
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
                history += f"Student: {content}\\n"
            elif role in ["assistant", "mwalimu"]:
                history += f"Mwalimu AI: {content}\\n"

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
                "X-Title": "Mwalimu AI Chat Engine",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter Gateway Connection Error: {e}")
        return f"Mambo! Mwalimu is having trouble connecting to the network right now: {e}"

def generate_quiz(topic, student, difficulty="Medium"):
    """Generates a structured dynamic 5-question multi-choice evaluation list via OpenRouter models."""
    difficulty_rules = {
    "Beginner": "Focus on foundational recognition, recalling basic definitions, direct matching, and basic counting with explicit hints.",
    "Intermediate": "Focus on application scenarios, multi-step problem solving, simple comparative relationships, and foundational word problems.",
    "Advanced": "Focus on critical thinking, complex contextual word problems, combining cross-topic parameters, and logical reasoning structures."
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
  {{
    "question": "Second Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "The exact correct option string matching one of the options"
  }},
  ... up to 5 elements total
]
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "[https://mwalimu-ai.streamlit.app](https://mwalimu-ai.streamlit.app)",
                "X-Title": "Mwalimu AI Quiz Engine",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        # FIX: Safely unpack content with a fallback empty string to prevent Pylance None type warnings
        raw_content = response.choices[0].message.content
        clean_content = (raw_content if raw_content is not None else "").strip()
        
        if clean_content.startswith("```json"):
            clean_content = clean_content.replace("```json", "", 1).rstrip("```")
        elif clean_content.startswith("```"):
            clean_content = clean_content.strip("```")
            
        return json.loads(clean_content.strip())
    except Exception as e:
        print(f"OpenRouter Quiz Engine Parsing Exception: {e}")
        return [
            {
                "question": f"Let's test your baseline understanding of {topic}. What is the primary focus of this subject area?",
                "options": ["Option A: Base Core Exploration", "Option B: Secondary Extension", "Option C: Applied Practical Analysis", "Option D: None of the above"],
                "answer": "Option C: Applied Practical Analysis"
            }
        ]

def generate_study_plan(student: dict, stats: dict) -> str:
    """Crafts an optimized personalized study timetable map strategy framework."""
    # 1. Safely extract the preferred language from the student profile dictionary
    preferred_language = student.get("language", "English")
    
    language_rules = {
        "English": "Write the entire response, explanations, and instructions in clear, grammatically correct English suitable for a student.",
        "Kiswahili": "Write the complete explanation, study milestones, and feedback loop text in clear, standard Kiswahili. Keep technical terms in brackets if necessary.",
        "Sheng": "Use casual, friendly conversational Sheng mixed with standard educational English guidelines to keep the student deeply engaged, but ensure the core biological/mathematical facts remain highly accurate."
    }
    
    # 2. Map the language rules instruction string safely
    target_language_instruction = language_rules.get(preferred_language, language_rules["English"])
    
    # 3. Construct the dynamic optimization prompt
    prompt = f"""
You are Mwalimu AI, an intelligent Kenyan teacher.
Create a personalized DAILY STUDY PLAN.

Student Profile
Name: {student.get("name", "Student")}
Grade: {student.get("grade", "N/A")}
Age: {student.get("age", "N/A")}
Learning Style: {student.get("learning_style", "General")}
Preferred Language: {preferred_language}

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Strand: {student.get("strand", "General")}
Sub-strand: {student.get("sub_strand", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

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
- {target_language_instruction}
- Write the entire plan in plain, natural format.
- NEVER use "Lorem ipsum", placeholder words, or dummy text.
- NEVER include bracketed source numbers or tokens. All content must be completely real and readable.
"""

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://mwalimu-ai.streamlit.app",
                "X-Title": "Mwalimu AI Study Planner",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 4. CRITICAL FIX: Extract content safely and guarantee a string return type using fallback
        raw_content = response.choices[0].message.content
        return raw_content if raw_content is not None else "Error: Mwalimu AI received an empty study plan from the generation model."
        
    except Exception as e:
        return f"Could not sync study strategy roadmap recommendations: {e}"

def generate_flashcards(topic, student):
    """Produces structured dynamic flashcard items using strict JSON formats."""
    prompt = f"""
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

Create exactly 10 revision flashcards about: {topic}
Return ONLY valid JSON.

Format:
[
  {{
    "question": "...",
    "answer": "..."
  }}
]

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Strand: {student.get("strand", "General")}
Sub-strand: {student.get("sub_strand", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

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
                "X-Title": "Mwalimu AI Flashcard Processor",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        # FIX: Safely unpack content with a fallback empty string to prevent Pylance None type warnings
        raw_content = response.choices[0].message.content
        clean_content = (raw_content if raw_content is not None else "").strip()
        
        if clean_content.startswith("```json"):
            clean_content = clean_content.replace("```json", "", 1).rstrip("```")
        elif clean_content.startswith("```"):
            clean_content = clean_content.strip("```")
            
        return json.loads(clean_content.strip())
    except Exception as e:
        print(f"Flashcard Generator Engine Parsing Error: {e}")
        return [
            {"question": f"What is the core baseline principle behind {topic}?", "answer": "Refer to your standard class curriculum documentation notes for context definitions."}
        ]

def generate_lesson(topic, student):
    """Builds interactive lesson explanations targeted to the student's active profile variables."""
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

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Strand: {student.get("strand", "General")}
Sub-strand: {student.get("sub_strand", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

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
                "HTTP-Referer": "[https://mwalimu-ai.streamlit.app](https://mwalimu-ai.streamlit.app)",
                "X-Title": "Mwalimu AI Lesson Plan Engine",
            },
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter Lesson Generation Error: {e}")
        return f"Mwalimu encountered an issue preparing your lesson roadmap: {e}. Please click generate again!"