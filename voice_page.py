# voice_page.py
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice import speech_to_text
from services.ai import ask_mwalimu
from services.database import save_chat_message

def render_voice_tutor_page(client):
    st.title("🎙️ Mwalimu AI - Voice Tutor")
    st.write("Click the microphone below to talk with your AI Teacher. Speak clearly!")

    # Extract student profile properties from session state
    name = st.session_state.get("student_name", "Student")
    grade = st.session_state.get("grade", "Grade 7")
    age = st.session_state.get("age", 10)
    favorite_subject = st.session_state.get("favorite_subject", "General")
    weak_subject = st.session_state.get("weak_subject", "")
    learning_style = st.session_state.get("learning_style", "Interactive")
    language = st.session_state.get("language", "English")

    student = {
        "name": name, "grade": grade, "age": age,
        "favorite_subject": favorite_subject, "weak_subject": weak_subject,
        "learning_style": learning_style, "language": language
    }

    # Persistent Pipeline State
    if "user_spoken_text" not in st.session_state:
        st.session_state.user_spoken_text = ""
    if "mwalimu_response_text" not in st.session_state:
        st.session_state.mwalimu_response_text = ""

    # Audio capturing processing hub button widget
    audio = mic_recorder(
        start_prompt="🎙️ Click & Start Speaking",
        stop_prompt="🛑 Stop & Send",
        key='recorder'
    )

    if audio:
        with st.spinner("Transcribing your voice..."):
            transcription = speech_to_text(audio['bytes'])
            if transcription and transcription != st.session_state.user_spoken_text:
                st.session_state.user_spoken_text = transcription
                st.session_state.mwalimu_response_text = ""  # Force recalculation update
                st.session_state.chat_history.append({"role": "user", "content": transcription})
                save_chat_message(name, grade, age, "user", transcription)

    # STEP 2: Render user speech text & trigger LLM context pipelines
    if st.session_state.user_spoken_text:
        st.info(f"🗣️ **What you said:** {st.session_state.user_spoken_text}")
        
        if not st.session_state.mwalimu_response_text:
            with st.spinner("🧙‍♂️ Mwalimu is thinking..."):
                try:
                    adaptive_context = f"Learning Style: {learning_style}, Favorite Subject: {favorite_subject}"
                    ai_response_text = ask_mwalimu(
                        question=st.session_state.user_spoken_text,
                        student=student,
                        messages=st.session_state.chat_history[:-1],
                        adaptive_context=adaptive_context
                    )
                    if ai_response_text:
                        ai_response_text = ai_response_text.replace("User Safety: safe", "").strip()
                        st.session_state.mwalimu_response_text = ai_response_text
                        st.session_state.chat_history.append({"role": "assistant", "content": ai_response_text})
                        save_chat_message(name, grade, age, "assistant", ai_response_text)
                    else:
                        st.session_state.mwalimu_response_text = "Mambo! I missed that, let's try again."
                except Exception as e:
                    st.error(f"Mwalimu setup issue: {str(e)}")

    # STEP 3: Display clean response text
    if st.session_state.mwalimu_response_text:
        st.success(f"🧙‍♂️ **Mwalimu:** {st.session_state.mwalimu_response_text}")