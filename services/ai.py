# services/ai.py
import os
import json
import random
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_layer import MwalimuKnowledgeLayer, clean_and_parse_json
# 1. Load keys from local .env file if it exists
load_dotenv()
knowledge_base = MwalimuKnowledgeLayer()
# 2. Unified fallback: check system environment variables first, then fallback to Streamlit secrets
api_key = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

# 3. Initialize unified OpenRouter gateway client safely
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key if api_key else "MOCK_KEY"
)

def ask_mwalimu(question, student, messages, adaptive_context=""):
    """Dispatches prompts to a specific high-quality free model on OpenRouter."""
    """Handles real-time conversational Q&A locked to the local curriculum guide framework."""
    subject = student.get('subject', 'Mathematics')
    topic = student.get('topic', 'Whole Numbers')
    sub_topic = student.get('sub_topic', 'Place Value')
    kicd_data = knowledge_base.get_curriculum_context(subject, topic, sub_topic)
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
You are Mwalimu AI, an empathetic and highly skilled Kenyan learning assistant. 
Your teaching approach must strictly align with the Kenya Institute of Curriculum Development (KICD) Competency-Based Curriculum (CBC) framework.
Adapt your explanations, complexity, vocabulary, and tone to match the specific student profile and learning context provided below.
You are currently helping the student with the topic: '{topic} ({sub_topic})' for Grade {student.get('grade')}.

=== KICD VERIFIED KNOWLEDGE ===
- Definition to uphold: {kicd_data['definition']}
- Intended outcomes: {', '.join(kicd_data['learning_objectives'])}

=== STUDENT PROFILE ===
Name: {student.get("name", "Student")}
Grade: {student.get("grade", "N/A")}
Age: {student.get("age", "N/A")}
Preferred Language: {student.get("preferred_language", "English")}
Favorite Subject: {student.get("favorite_subject", "N/A")}
Weak Subject: {student.get("weak_subject", "N/A")}
Learning Style: {student.get("learning_style", "General")}
Language: {student.get("language", "English")}

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Topic: {student.get("topic", "General")}
Sub-topic: {student.get("sub_topic", "General")}
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
- Avoid overly complex explanations; break down concepts into simple, digestible steps.
- Ensure all responses are culturally relevant and appropriate for the Kenyan context.
- Use localized Kenyan examples where applicable (e.g., local currency, towns, context) to keep it relatable.
- Teach or answer questions using the active context topic.
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

def generate_quiz(topic, student, difficulty="Easy"):
    """Generates structured JSON quiz variations based on adaptive parameters."""
    difficulty_rules = {
        "Easy": "Use very simple language. Focus on one core concept per question. No trick questions.",
        "Medium": "Slightly more challenging. Require two-step thinking. Use localized practical examples.",
        "Hard": "Incorporate complex application questions, critical thinking scenarios, and higher-order reasoning."
    }

    subject = student.get('subject', 'Mathematics')
    sub_topic = student.get('sub_topic', 'Place Value')
    
    # Extract ground truth from the Local Knowledge Layer
    kicd_data = knowledge_base.get_curriculum_context(subject, topic, sub_topic)
    past_papers = knowledge_base.get_past_papers_context(subject, topic)
    
    prompt = f"""
You are Mwalimu AI, an expert Examiner specializing in the Kenyan KICD Competency-Based Curriculum (CBC) framework. 
Your task is to generate a highly contextual, age-appropriate practice quiz based on the student's current learning topic.

Generate a multiple-choice quiz about '{topic}' for a student in {student.get('grade')} ({student.get('age')} years old).

=== GROUND TRUTH KNOWLEDGE LAYER ===
Use the following verified rules and definitions to construct your questions. Do not deviate from these concepts:
- Definition Focus: {kicd_data['definition']}
- Target Learning Goals: {', '.join(kicd_data['learning_objectives'])}
- Reference Past Examination Structures: {json.dumps(past_papers)}
CRITICAL CONTEXT RULES:
- Every math word problem MUST contain all necessary numerical information to be solvable (e.g., do not say 'if each plant produces 2', specify the total number of plants first!).
- Use Kenyan names (e.g., Mwangi, Amina), locations, and real-world local scenarios (M-Pesa, market stalls, matatus) to make the word problems relatable.
- Match the cognitive expectations of a {student.get('grade')} student under CBC guidelines.
- Write the text strictly in the student's preferred language: {student.get('language', 'English')}.

Target Difficulty Level: {difficulty}
Difficulty Context Rules: {difficulty_rules.get(difficulty, "")}
Preferred Learning Style: {student.get('learning_style', 'General')}

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

CRITICAL OPTION CONSTRAINT RULES:
1. **No Math Formulations**: Every element in the "options" array MUST be a fully calculated, single final value (e.g., use "48,878 shillings", NEVER "45,678 + 3,200 shillings").
2. **Realistic Distractors**: Make the incorrect options plausible calculation errors (like missing a carry-over digit or accidentally subtracting instead of adding) so students are challenged to think critically.
3. Every math word problem MUST contain all necessary numerical information to be solvable.
4. For Mathematics (Whole Numbers), ensure all intermediate and final calculation results are strictly positive WHOLE NUMBERS. Avoid division problems that result in fractional remainders or decimals.
5. Use Kenyan names (e.g., Mwangi, Amina), locations, and real-world local scenarios (M-Pesa, market stalls, matatus) to make the word problems relatable.
6. Match the cognitive expectations of a {student.get('grade')} student under CBC guidelines.
7. Write the text strictly in the student's preferred language: {student.get('language', 'English')}.
8. **Consistent Units**: Ensure all options include the correct unit matching the question (e.g., "shillings", "passengers").
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

def generate_study_plan(student: dict, stats: dict) -> str:
    """Crafts an optimized personalized study timetable map strategy framework."""
    # 1. Safely extract the preferred language from the student profile dictionary
    preferred_language = student.get("language", "English")
    subject = student.get('subject', 'Mathematics')
    topic = student.get('topic', 'Whole Numbers')
    sub_topic = student.get('sub_topic', 'Place Value')
    
    milestones = knowledge_base.get_study_milestones(subject, topic, sub_topic)
    language_rules = {
        "English": "Write the entire response, explanations, and instructions in clear, grammatically correct English suitable for a student.",
        "Kiswahili": "Write the complete explanation, study milestones, and feedback loop text in clear, standard Kiswahili. Keep technical terms in brackets if necessary.",
        "Sheng": "Use casual, friendly conversational Sheng mixed with standard educational English guidelines to keep the student deeply engaged, but ensure the core biological/mathematical facts remain highly accurate."
    }
    
    # 2. Map the language rules instruction string safely
    target_language_instruction = language_rules.get(preferred_language, language_rules["English"])
    
    # 3. Construct the dynamic optimization prompt
    prompt = f"""
You are Mwalimu AI, an expert Academic Counselor and Curriculum Planner specializing in the Kenyan KICD Competency-Based Curriculum (CBC) framework. 
Your goal is to build a highly actionable, structured, and realistic Personalized Study Plan based on the student's specific profile.

Student Profile
Name: {student.get("name", "Student")}
Grade: {student.get("grade", "N/A")}
Age: {student.get("age", "N/A")}
Learning Style: {student.get("learning_style", "General")}
Preferred Language: {preferred_language}


=== KICD GROUND TRUTH MILESTONES ===
You MUST anchor your schedule layout directly on these local milestone profiles:
{json.dumps(milestones)}

=== ACTIVE CBC CURRICULUM CONTEXT ===
Subject: {student.get("subject", "General")}
Topic: {student.get("topic", "General")}
Sub-topic: {student.get("sub_topic", "General")}
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
7. **Learning Style Integration**: Tailor study methods to their Learning Style. For example, if they are "Visual", include instructions to draw mind maps; if they are "Auditory/Interactive", suggest reading aloud or explaining concepts to a friend.
8. A dynamic custom Quiz recommendation
9. A warm, motivational message using encouraging Kenyan teacher phrasing using their preferred language (e.g., "Kazi safi", "Siku Njema", "Tia bidii", "Keep pushing").
10.Write the output text STRICTLY in clean {student.get("preferred_language", "English")}. Do not use foreign language tokens or corrupted text.
11. NEVER use HTML line breaks like '<br>' or tags anywhere in the text or tables.
12. When giving motivational messages, always use clean {student.get("preferred_language", "English")} and avoid any slang or informal text that could be misinterpreted.

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

def generate_flashcards(topic, student, difficulty="Medium"):
    """Produces structured dynamic flashcard items using strict JSON formats."""
    difficulty_rules = {
    "Beginner": "Focus on foundational recognition, recalling basic definitions, direct matching, and basic counting with explicit hints.",
    "Intermediate": "Focus on application scenarios, multi-step problem solving, simple comparative relationships, and foundational word problems.",
    "Advanced": "Focus on critical thinking, complex contextual word problems, combining cross-topic parameters, and logical reasoning structures."
}
    subject = student.get('subject', 'Mathematics')
    topic = student.get('topic', 'Whole Numbers')
    sub_topic = student.get('sub_topic', 'Place Value')

    verified_deck = knowledge_base.get_flashcards_context(subject, topic, sub_topic)
    kicd_data = knowledge_base.get_curriculum_context(subject, topic, sub_topic)
    prompt = f"""
You are Mwalimu AI, an expert Examiner specializing in the Kenyan KICD Competency-Based Curriculum (CBC) framework. 
Your task is to generate a highly contextual, age-appropriate practice quiz based on the student's current learning topic.

Generate a multiple-choice quiz about '{topic}' for a student in {student.get('grade')} ({student.get('age')} years old).

=== CURRICULUM DATA BASELINE ===
Anchor your facts on this verified knowledge data:
- Core Definition: {kicd_data['definition']}
- Pre-approved Deck Flashcards: {json.dumps(verified_deck)}

CRITICAL STRUCTURE RULE: You MUST generate exactly 5 distinct multiple-choice questions. 

Target Difficulty Level: {difficulty}
Difficulty Context Rules: {difficulty_rules.get(difficulty, "")}
Preferred Learning Style: {student.get('learning_style', 'General')}
Preferred Delivery Language: {student.get('language', 'English')}
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
Topic: {student.get("topic", "General")}
Sub-topic: {student.get("sub_topic", "General")}
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
Topic: {student.get("topic", "General")}
Sub-topic: {student.get("sub_topic", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

Rules:
- Grade appropriate
- Simple language
- No markdown wrappers around json array
- No explanations
- No extra text
- **Context**: Use Kenyan names, locations, and real-world local scenarios to make the word problems relatable.
- **Difficulty**: Match the cognitive expectations of a {student.get('grade')} student under CBC guidelines.
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
    """Generates full structural markdown lessons backed by the local KICD Knowledge Base."""
    subject = student.get('subject', 'Mathematics')
    topic = student.get('topic', 'Whole Numbers')
    sub_topic = student.get('sub_topic', 'Place Value')
    
    # Extract ground truth context fields
    kicd_data = knowledge_base.get_curriculum_context(subject, topic, sub_topic)
    prompt = f"""
You are Mwalimu AI, an inspiring and expert Senior School Teacher specializing in the Kenyan KICD Competency-Based Curriculum (CBC). 
Your task is to generate a comprehensive, highly engaging, and structured lesson text for a student based on their profile and selected curriculum pathway.

=== CBC KNOWLEDGE LAYER INJECTION ===
You MUST build your lesson around this verified ground-truth data payload:
- Target Concept Definition: {kicd_data['definition']}
- Verified Step-by-Step Worked Examples: {json.dumps(kicd_data['worked_examples'])}

=== STUDENT PROFILE ===
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
Topic: {student.get("topic", "General")}
Sub-topic: {student.get("sub_topic", "General")}
Learning Outcome Target: {student.get("learning_outcome", "General")}

=== LESSON ARCHITECTURE RULES ===
Please construct the lesson using clean Markdown headers. The lesson MUST include the following 9 numbered sections in order:

## 1. Lesson Title
- Create an exciting and clear title incorporating the active topic.

## 2. Learning Objectives
- State 3 or 4 clear bullet points outlining what the student will be able to do after completing this lesson, directly matching the Learning Outcome Target.

## 3. Introduction
- Hook the student's interest using a friendly greeting using Kenyan phrases (e.g., "Mambo!", "Habari!", or welcoming them by name: {student.get("name")}) and relate the topic to everyday life.

## 4. Main Explanation
- Breakdown the core concepts clearly. Use simple language and vocabulary appropriate for a {student.get('grade')} student.
- Adapt the explanation explicitly to a {student.get('learning_style')} learning style.

## 5. Real-life Kenyan Examples
- Ground the concept with relatable Kenyan contextual examples (e.g., matatus, market scenarios like Mama Mboga, local food like ugali/sukuma wiki, M-Pesa, or athletics/running tracking).

## 6. Worked Examples
- Provide step-by-step solutions to 1 or 2 practical problems or case scenarios illustrating the concept.

## 7. Practice Questions
- Provide 3 progressive questions matching the difficulty of the lesson to encourage active recall and critical thinking. Do not provide the answers immediately.

## 8. Summary & Fun Fact
- Bullet points summarizing the main takeaways of the lesson, followed by an interesting, mind-blowing fun fact relating to the topic.

## 9. Homework
- Create an engaging practical activity or mini-assignment that the student can perform at home or around the house to observe the concept in action.

=== STRICT GUIDELINES ===
- Always match the vocabulary to {student.get('grade')} expectations.
- Write primarily in the preferred language: {student.get('language')}.
- Do not append any meta-commentary, safety labels ("User Safety: safe"), or extra prompt diagnostics. Output only the complete lesson content starting directly from the Lesson Title.
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