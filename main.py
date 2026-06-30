# main.py
import base64
import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Load environmental configurations
load_dotenv()

# --- STREAMLIT PAGE CONFIGURATION (MUST BE ABSOLUTE FIRST COMMAND)
st.set_page_config(
    page_title="Mwalimu AI App",
    page_icon="assets/logo112.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Core Module Imports (Mapped to your true local path directory structure)
from services.ai import ask_mwalimu, generate_quiz, generate_study_plan, generate_flashcards, generate_lesson
from services.database import (
    create_tables,
    save_activity,
    get_student_stats,
    get_student_quiz_history,
    get_next_difficulty,
    get_student_learning_analysis,
    get_chat_history,
    save_chat_message,
    clear_student_chat_history
)
from voice_page import render_voice_tutor_page
from config import CBC # Dynamic CBC repository dictionary

# Initialize Database Architecture
create_tables()

# --- INITIALIZE STATE FROM DATABASE & INPUT WORKSPACE ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Main Chat"
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_raw_score" not in st.session_state:
    st.session_state.quiz_raw_score = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "study_plan" not in st.session_state:
    st.session_state.study_plan = None
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "lesson_content" not in st.session_state:
    st.session_state.lesson_content = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize client using the environment variable configuration setup
@st.cache_resource
def get_backend_client():
    return os.environ.get("OPENROUTER_API_KEY")
client = get_backend_client()

# --- BASE64 SIDEBAR IMAGE INJECTOR ---
try:
    with open("assets/logo211.png", "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    sidebar_bg_style = f"background-image: url('data:image/png;base64, {encoded_logo}') !important;"
except Exception:
    sidebar_bg_style = ""

# GLOBAL UI & CSS LAYOUT SETTINGS
st.html(f"""
<style>
@media (min-width: 768px) {{
[data-testid="stHeader"], header {{ background-color: transparent !important; height: 3.5rem !important; }}
[data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {{ margin-top: -1.5rem !important; padding-top: 0rem !important; }}
[data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"], .block-container {{ padding-top: 1.5rem !important; margin-top: 0rem !important; }}
}}
@media (max-width: 767px) {{
[data-testid="stHeader"], header {{ background-color: transparent !important; height: 3.5rem !important; }}
[data-testid="stAppViewMainObj"], .stMain, [data-testid="stMain"] {{ margin-top: 0rem !important; padding-top: 0.5rem !important; }}
}}
[data-testid="stMainBlockContainer"], [data-testid="stAppViewBlockContainer"], .block-container {{ padding-top: 1rem !important; }}
[data-testid="stHeader"] button {{ background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 4px !important; z-index: 999999 !important; }}
[data-testid="stSidebarUserContent"] {{ padding-top: 0rem !important; margin-top: 0rem !important; }}
[data-testid="stSidebarHeader"] {{
padding-top: 0.5rem !important; padding-bottom: 0.5rem !important; margin-bottom: 0rem !important; min-height: 80px !important;
{sidebar_bg_style} background-size: contain !important; background-repeat: no-repeat !important; background-position: left center !important; margin-left: 55px !important;
}}
/* --- ATTRACTIVE GLOBAL BUTTON HOVER OVERRIDES --- */
div.stButton > button {{
transition: all 0.2s ease-in-out !important;
}}
div.stButton > button:hover {{
border-color: #1E3A8A !important;
color: #1E3A8A !important;
box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1) !important;
}}
</style>
""")

# ==========================================
# 🎯 CLEANED SIDEBAR CONFIGURATION
# ==========================================
# (Removed duplicate header titles here — Logo will render directly at the top of the sidebar panel)
raw_name = st.sidebar.text_input("Student Name", value=st.session_state.get("student_name") or "")
name = raw_name.strip().title() if raw_name else ""
grade = st.sidebar.selectbox("Grade", [
    "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6",
    "Grade 7", "Grade 8", "Form 1", "Form 2", "Form 3", "Form 4"
], index=0)
age = st.sidebar.number_input("Age", min_value=5, max_value=25, value=10)
favorite_subject = st.sidebar.text_input("Favorite Subject", value=st.session_state.get("favorite_subject") or "")
weak_subject = st.sidebar.text_input("Weak Subject", value=st.session_state.get("weak_subject") or "")
learning_style = st.sidebar.selectbox("Learning Style", ["Visual", "Practical", "Reading/Writing", "Interactive", "Story-based"])
language = st.sidebar.selectbox("Preferred Language", ["English", "Kiswahili", "Sheng"])

if name:
    st.session_state.student_name = name
    try:
        historical_chats = get_chat_history(name, grade, int(age))
        if historical_chats and not st.session_state.chat_history:
            st.session_state.chat_history = historical_chats
    except Exception as db_err:
        print(f"Database restoration skipped on initialization: {db_err}")

# CBC CURRICULUM INTEGRATION SELECTORS
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Curriculum Context")

subjects = list(CBC.get(grade, {}).keys()) or ["General Studies"]
subject = st.sidebar.selectbox("Subject", subjects)

topics = list(CBC.get(grade, {}).get(subject, {}).keys()) or ["General Topic"]
topic = st.sidebar.selectbox("Topic", topics)

sub_topics = list(CBC.get(grade, {}).get(subject, {}).get(topic, {}).keys()) or ["General Sub-Topic"]
sub_topic = st.sidebar.selectbox("Sub-topic", sub_topics)

outcomes = CBC.get(grade, {}).get(subject, {}).get(topic, {}).get(sub_topic, []) or ["General Learning Outcome"]
learning_outcome = st.sidebar.selectbox("Learning Outcome", outcomes)

# Assemble Complete Multi-Dimensional Student Object Map
student = {
    "name": name if name else "Student",
    "grade": grade,
    "age": int(age),
    "favorite_subject": favorite_subject,
    "weak_subject": weak_subject,
    "learning_style": learning_style,
    "language": language,
    "subject": subject,
    "topic": topic,
    "sub_topic": sub_topic,
    "learning_outcome": learning_outcome
}

# --- ACTIVE PROFILE CARD ---
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Active Profile")
if name:
    st.sidebar.info(f"**Student:** {name} \n\n**{grade}** | **Age:** {age}")
else:
    st.sidebar.warning("Please type your Student Name at the top of the sidebar.")

# --- NAVIGATION HUB ---
st.sidebar.subheader("🚀 Navigation Hub")
if st.sidebar.button("Voice Tutor Mode", use_container_width=True):
    st.session_state.current_page = "Voice Tutor"
    st.rerun()

if st.sidebar.button("🗑️Clear Chat",):
    if name and name.strip() != "":
        try:
            clear_student_chat_history(name, grade, int(age))
        except Exception as e:
            print(f"Error clearing database chat logs: {e}")
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.quiz = None
    st.session_state.quiz_submitted = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_raw_score = 0
    st.session_state.flashcards = []
    st.session_state.lesson_content = None
    st.rerun()

# --- SIDEBAR PROGRESS DASHBOARD GENERATION ---
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Progress Dashboard")
if name:
    stats = get_student_stats(name, grade, age)
    st.sidebar.metric("Questions Asked", stats.get("questions", 0))
    st.sidebar.metric(label="Quizzes Taken", value=stats["quizzes"])
    st.sidebar.metric("Average Score", f"{stats.get('average_score', 0)}%")
    
    stats = get_student_stats(name, grade, int(age))
    analysis = get_student_learning_analysis(name, grade, age)
    st.sidebar.markdown(f"**Learning Status:** `{analysis.get('current_level', 'Medium')}`")
    
    if analysis.get('weak_topics'):
        st.sidebar.markdown("**Needs Improvement:**")
        for t in analysis['weak_topics']:
            st.sidebar.caption(f"⚠️ {t}")
            
    if analysis.get('strong_topics'):
        st.sidebar.markdown("**Mastered Areas:**")
        for t in analysis['strong_topics']:
            st.sidebar.caption(f"✅ {t}")
            
    history_scores = get_student_quiz_history(name, grade, age)
    if len(history_scores) > 0:
        st.sidebar.markdown("**Performance Trend**")
        st.sidebar.line_chart(history_scores)
else:
    st.sidebar.caption("Fill in your name to start tracking parameters.")


# ==========================================
# 🧙‍♂️ MAIN BRANDING HEADER CONTAINER
# ==========================================
col1, col2 = st.columns([1, 5], vertical_alignment="center")
with col1:
    try:
        title_logo = Image.open("assets/logo112.png")
        st.image(title_logo, width=100)
    except Exception:
        pass
with col2:
    st.markdown("<h1 style='margin-top: 0 !important; margin-bottom: 0 !important; padding: 0;'>Mwalimu AI App</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top: 2px !important; margin-bottom: 0 !important; color: gray; font-weight: normal;'>Shaping Minds, Shifting Futures.</h4>", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
st.write("Welcome to Mwalimu AI! 🇰🇪 I am your friendly, adaptive Kenyan AI teacher. To begin, create your student profile in the sidebar to sync your learning. From there, you can ask me any school question, explore real-time interactive lessons, challenge yourself with 5-question targeted quizzes, or launch into Voice Tutor Mode for an immersive audio learning experience tailored precisely to your grade, learning style, and topic tracking!")

# DISPLAY ACTIVE CBC TARGET TRACKER BOX AT TOP OF PAGE
if name:
    st.markdown(
        f"""
        <div style="background-color: #1e293b; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <span style="color: #3b82f6; font-weight: bold;">Active Curriculum Targeting:</span>
        <span style="color: #f8fafc;">Grade {grade} &bull; Subject: {subject} &bull; Topic: {topic} &bull; Sub-topic: {sub_topic}</span>
        <br>
        <span style="color: #94a3b8; font-weight: bold;">Target Learning Outcome:</span> 
        <span style="color: #f8fafc;">{learning_outcome}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

# =======================================================
# PAGE VIEW MODE 1: MAIN CHAT DASHBOARD
# =======================================================
if st.session_state.current_page == "Main Chat":
    st.markdown("---")
    if st.button("Go to Quizzes, Flashcards & Lessons Generators", use_container_width=True):
        st.session_state.current_page = "Generators Hub"
        st.rerun()
    
    # --- AI STUDY PLAN SECTION
    st.markdown("---")
    st.subheader("AI Personalized Study Plan")
    if st.button("Generate Today's Study Plan", use_container_width=True):
        if not name:
            st.warning("Please create Student Profile in the sidebar first!")
        else:
            with st.spinner("Creating your personalized study plan..."):
                stats = get_student_stats(name, grade, int(age))
                st.session_state.study_plan = generate_study_plan(student, stats)
                st.rerun()
    
    if st.session_state.study_plan:
        st.info("Tip: Follow the allocated time intervals for maximum focus today!")
        st.markdown(st.session_state.study_plan)
        if st.button("Clear Study Plan"):
            st.session_state.study_plan = None
            st.rerun()

    # --- CHAT WITH MWALIMU SECTION
    st.markdown("---")
    st.write("### Chat with Mwalimu")
    
    for msg in st.session_state.chat_history:
        role_label = "user" if msg["role"] in ["student", "user"] else "assistant"
        with st.chat_message(role_label):
            st.write(msg["content"])
            
    if user_question := st.chat_input("Ask your question"):
        if not name:
            st.warning("Please create Student Profile in the sidebar first!")
        else:
            st.session_state.chat_history.append({"role": "student", "content": user_question})
            save_chat_message(name, grade, int(age), "student", user_question)
            
            try:
                save_activity(
                    student_name=name, 
                    student_grade=grade, 
                    student_age=int(age), 
                    activity_type="chat", 
                    topic=topic, 
                    score=0, 
                    subject=subject, 
                    sub_topic=sub_topic,
                    learning_outcome=learning_outcome
                )
            except Exception as db_err:
                print(f"Database logging background error: {db_err}")
            
            stats = get_student_stats(name, grade, int(age))
            analysis = get_student_learning_analysis(name, grade, int(age))
            
            adaptive_context = f"""
            Current Mastery Level: {analysis.get('current_level', 'Medium')}
            Average Quiz Score: {stats.get('average_score', 0)}%
            Weak Topics: {', '.join(analysis.get('weak_topics', [])) if analysis.get('weak_topics') else 'None'}
            Strong Topics: {', '.join(analysis.get('strong_topics', [])) if analysis.get('strong_topics') else 'None'}
            """
            
            with st.spinner("Mwalimu is thinking..."):
                try:
                    response = ask_mwalimu(
                        question=user_question, student=student,
                        messages=st.session_state.chat_history[:-1], adaptive_context=adaptive_context
                    )
                    if not response:
                        response = "Mambo! I received an empty response. Let's try asking that again."
                except Exception as e:
                    response = f"Mwalimu configuration error: {str(e)}"
            
            response = response.replace("User Safety: safe", "").strip()
            response = response.replace("User Safety:safe", "").strip()
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            save_chat_message(name, grade, int(age), "assistant", response)
            st.rerun()

# =======================================================
# PAGE VIEW MODE 2: VOICE TUTOR DASHBOARD MODE
# =======================================================
elif st.session_state.current_page == "Voice Tutor":
    st.markdown("---")
    if st.button("Back to Main Chat Dashboard", use_container_width=True, key="back_from_voice"):
        st.session_state.current_page = "Main Chat"
        st.rerun()
    if not name:
        st.warning("Please enter your name in the Student Profile registration section to unlock the Voice Tutor engine.")
    else:
        render_voice_tutor_page(client)

# =======================================================
# PAGE VIEW MODE 3: GENERATORS WORKSPACE HUB
# =======================================================
elif st.session_state.current_page == "Generators Hub":
    st.markdown("---")
    if st.button("Go back to Main Chat Dashboard", use_container_width=True, key="back_from_generators"):
        st.session_state.current_page = "Main Chat"
        st.rerun()
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Quiz Generator Engine", "AI Flashcards Maker", "AI Lessons Generator"])
    
    with tab1:
        st.subheader("Quiz Generator")
        quiz_topic = st.text_input("Quiz Topic", placeholder="Defaults to current dynamic Sub topic selection", value=sub_topic, key="workspace_quiz_topic")
        
        if st.button("Generate Quiz", use_container_width=True):
            if not quiz_topic.strip():
                st.warning("Please enter a quiz topic.")
            elif not name:
                st.warning("Please create Student Profile in the sidebar first!")
            else:
                with st.spinner("Generating quiz..."):
                    target_diff = get_next_difficulty(name, grade, int(age), quiz_topic)
                    st.session_state.quiz = generate_quiz(quiz_topic, student, target_diff)
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_raw_score = 0
                
                save_activity(
                    student_name=name, 
                    student_grade=grade, 
                    student_age=int(age),
                    activity_type="quiz_generation", 
                    topic=quiz_topic, 
                    score=0,
                    subject=subject,
                    topics=topic, 
                    sub_topic=sub_topic, 
                    learning_outcome=learning_outcome
                )
                st.rerun()
        
        if st.session_state.quiz:
            st.markdown("### Generated Quiz")
            for i, question in enumerate(st.session_state.quiz):
                st.markdown(f"#### Question {i+1}")
                st.radio(
                    question["question"],
                    question["options"],
                    index=None,
                    key=f"q_{i}",
                    disabled=st.session_state.quiz_submitted
                )
            if not st.session_state.quiz_submitted:
                if st.button("Submit Quiz", use_container_width=True):
                    current_answers = [st.session_state.get(f"q_{i}") for i in range(len(st.session_state.quiz))]
                    if None in current_answers:
                        st.warning("Please answer all questions before submitting.")
                    else:
                        score = 0
                        for i, q in enumerate(st.session_state.quiz):
                            if current_answers[i] == q["answer"]:
                                score += 1
                        st.session_state.quiz_raw_score = score
                        st.session_state.quiz_score = round((score / len(st.session_state.quiz)) * 100)
                        st.session_state.quiz_submitted = True
                        save_activity(
                            student_name=name, student_grade=grade, student_age=int(age),
                            activity_type="quiz_score", topic=quiz_topic, 
                            score=st.session_state.quiz_score,
                            subject=subject, topics=topic, sub_topic=sub_topic, 
                            learning_outcome=learning_outcome
                        )
                        st.rerun()
            
            if st.session_state.quiz_submitted:
                raw_score = st.session_state.quiz_raw_score
                total_questions = len(st.session_state.quiz)
                percentage = st.session_state.quiz_score
                st.success(f"You scored {raw_score}/{total_questions} ({percentage}%)")
                st.markdown("## Answer Review")
                for i, q in enumerate(st.session_state.quiz):
                    student_answer = st.session_state.get(f"q_{i}")
                    correct_answer = q["answer"]
                    st.markdown(f"### Question {i+1}")
                    st.write(q["question"])
                    st.write(f"**Your Answer:** {student_answer}")
                    if student_answer == correct_answer:
                        st.success(f"Correct Answer: {correct_answer}")
                    else:
                        st.error(f"Correct Answer: {correct_answer}")
                if st.button("Clear Quiz Results", use_container_width=True):
                    st.session_state.quiz = None
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_raw_score = 0
                    st.rerun()

    with tab2:
        st.subheader("AI Flashcards Maker")
        flashcard_topic = st.text_input("Enter a topic for your flashcards:", value=sub_topic, key="fc_topic")
        if st.button("Generate Flashcards", use_container_width=True):
            if flashcard_topic.strip() == "":
                st.warning("Please enter a valid topic first!")
            elif not name:
                st.warning("Please create Student Profile in the sidebar first!")
            else:
                with st.spinner("Mwalimu AI is writing your flashcards..."):
                    st.session_state.flashcards = generate_flashcards(flashcard_topic, student)
                    st.rerun()
        if st.session_state.flashcards:
            st.markdown("---")
            st.info("Click **'Show Answer'** to test your active recall memory knowledge!")
            for i, card in enumerate(st.session_state.flashcards, start=1):
                st.markdown(f"### Flashcard {i}")
                st.write(f"**Question:** {card.get('question', '')}")
                with st.expander("Show Answer"):
                    st.success(f"**Answer:** {card.get('answer', '')}")
            st.markdown("---")
            if st.button("Clear Flashcards", use_container_width=True):
                st.session_state.flashcards = []
                st.rerun()

    with tab3:
        st.subheader("AI Lessons Generator")
        lesson_topic = st.text_input("Enter the topic you want to learn today:", value=learning_outcome, key="lesson_topic_input")
        if st.button("Generate Lesson", use_container_width=True):
            if lesson_topic.strip() == "":
                st.warning("Please enter a valid lesson topic first!")
            elif not name:
                st.warning("Please create Student Profile in the sidebar first!")
            else:
                with st.spinner("Mwalimu AI is preparing your personalized lesson..."):
                    try:
                        st.session_state.lesson_content = generate_lesson(lesson_topic, student)
                        save_activity(
                            student_name=name, student_grade=grade, student_age=int(age),
                            activity_type="lesson", topic=lesson_topic, score=0,
                            subject=subject, topics=topic, sub_topic=sub_topic, 
                            learning_outcome=learning_outcome
                        )
                    except Exception as e:
                        st.error(f"Failed to generate lesson: {str(e)}")
                    st.rerun()
        
        if "lesson_content" in st.session_state and st.session_state.lesson_content:
            st.markdown("---")
            st.info("Tip: Read through the breakdown below. Mwalimu customized this explanation precisely for your style!")
            lesson_text = st.session_state.lesson_content
            if isinstance(lesson_text, str):
                if lesson_text.startswith("```markdown"):
                    lesson_text = lesson_text.replace("```markdown", "", 1).rstrip("```")
                elif lesson_text.startswith("```"):
                    lesson_text = lesson_text.strip("```")
                st.markdown(lesson_text)
            else:
                st.write(lesson_text)
            if st.button("Clear Lesson Content", use_container_width=True):
                st.session_state.lesson_content = None
                st.rerun()

# --- FOOTER BRANDING TAGS ---
logo_html_tag = ""
logo_path = "assets/logo112.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    logo_html_tag = f'<img src="data:image/png;base64, {b64}" width="20" style="vertical-align: middle; margin-right: 8px;">'

st.markdown(
    f"""
    <hr style='margin-top: 50px; border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.2), rgba(0,0,0,0));'>
    <p style='color: gray; font-size: 0.85rem; display: flex; align-items: center; justify-content: center;'>
    {logo_html_tag} Mwalimu AI App Version 0.7 | CBC Curriculum Engine | © 2026 Copyright
    </p>
    """,
    unsafe_allow_html=True
)