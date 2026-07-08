# voice_page.py
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from voice import speech_to_text
from services.ai import ask_mwalimu
from services.database import save_chat_message

def render_voice_tutor_page(client):
    st.title("🎙️ Mwalimu AI - Voice Tutor")
    st.write("Click the microphone below to talk with your AI Teacher. Speak clearly!")

    # Track a version number to break the microphone's stubborn cache loop
    if "voice_recorder_version" not in st.session_state:
        st.session_state.voice_recorder_version = 0

    # Persistent Pipeline State Initialization
    if "user_spoken_text" not in st.session_state:
        st.session_state.user_spoken_text = ""
    if "mwalimu_response_text" not in st.session_state:
        st.session_state.mwalimu_response_text = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

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

    # Dynamic version keying breaks the cache loop
    audio = mic_recorder(
        start_prompt="🎙️ Click & Start Speaking",
        stop_prompt="🛑 Stop & Send",
        key=f"voice_recorder_v_{st.session_state.voice_recorder_version}"  
    )

    # State flag to keep track of errors across the runtime flow
    has_error = False

    if audio:
        with st.spinner("Transcribing your voice..."):
            transcription = speech_to_text(audio['bytes'])
            
            if transcription:
                # ─── CRITICAL CRASH & ERROR SHIELD GUARDRAIL ───
                error_keywords = ["failed", "402", "error", "client error", "payment required"]
                if any(keyword in transcription.lower() for keyword in error_keywords):
                    st.error(f"🛑 Transcription API Error: {transcription}")
                    st.info("💡 Mwalimu Tip: Your OpenRouter audio billing credits might be empty. Please check your dashboard balance!")
                    
                    # Log the error state in session memory so the bottom layout knows to render
                    if not st.session_state.chat_history:
                        st.session_state.chat_history.append({"role": "system", "content": "error_state_active"})
                    has_error = True

                # If it's a valid speech string, proceed safely
                elif transcription != st.session_state.user_spoken_text:
                    st.session_state.user_spoken_text = transcription
                    st.session_state.mwalimu_response_text = ""  
                    st.session_state.chat_history.append({"role": "user", "content": transcription})
                    save_chat_message(name, grade, age, "user", transcription)

    # Check existing history to catch an active error state on page refresh
    if any(msg.get("content") == "error_state_active" for msg in st.session_state.chat_history):
        has_error = True

    # STEP 2: Render user speech text & trigger LLM context pipelines (ONLY IF NO ERROR)
    if st.session_state.user_spoken_text and not has_error:
        st.info(f"🗣️ **What you said:** {st.session_state.user_spoken_text}")
        
        if not st.session_state.mwalimu_response_text:
            with st.spinner("🧙‍♂️ Mwalimu is thinking..."):
                try:
                    preferred_language = student.get("language", "English")
                    adaptive_context = f"Learning Style: {learning_style}, Favorite Subject: {favorite_subject}, Preferred Language: {preferred_language}"
                    
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

    # STEP 3: Display clean response text (ONLY IF NO ERROR)
    if st.session_state.mwalimu_response_text and not has_error:
        st.success(f"🧙‍♂️ **Mwalimu:** {st.session_state.mwalimu_response_text}")

    # ─── FIXED: THE DYNAMIC RESET BUTTON AT THE ABSOLUTE BOTTOM ───
    # Since we removed st.stop(), the script safely runs through here even on transcription crashes!
    if len(st.session_state.chat_history) > 0:
        st.write("")  # Clear vertical padding spacer
        if st.button("🧹 Clear Voice Session & Reset Cache"):
            st.session_state.user_spoken_text = ""
            st.session_state.mwalimu_response_text = ""
            st.session_state.chat_history = []
            st.session_state.voice_recorder_version += 1
            st.rerun()
