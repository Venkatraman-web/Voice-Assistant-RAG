import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
import app

r = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
# -----------------------------
# SESSION STATE
# -----------------------------

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "audio_text" not in st.session_state:
    st.session_state.audio_text = None

if "response" not in st.session_state:
    st.session_state.response = None


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("Navigation")

nav = st.sidebar.radio(
    "Go to",
    ["Setup Knowledge Base", "Voice Assistant"],
    index=0
)
# =============================
# DOCUMENT SETUP
# =============================

if nav == "Setup Knowledge Base":

    st.title("Knowledge Base Setup")

    file = st.file_uploader("Upload TXT or PDF")

    processdoc = st.button("Process Documents")

    if processdoc:

        if file is None:
            st.warning("Upload a document first")

        else:

            with st.spinner("Processing document..."):

                app.process_document(file)

            st.session_state.document_ready = True

            st.success(f"Processed {len(app.chunks)} document chunks")

# =============================
# VOICE ASSISTANT
# =============================

else:

    st.title("Voice Assistant RAG System")
    # -----------------------------
    # Voice Selection
    # -----------------------------

    voice = st.sidebar.selectbox(
        "Select Voice",
        ["David", "Zira"]
    )

    if voice == "David":
        engine.setProperty("voice", voices[0].id)
    else:
        engine.setProperty("voice", voices[1].id)

    duration = st.sidebar.slider(
        "Recording Duration (seconds)",
        min_value=1,
        max_value=10,
        value=5
    )

    # -----------------------------
    # RECORDING
    # -----------------------------

    start, process = st.columns(2)

    startbtn = start.button("Start Recording")
    processbtn = process.button("Process Recording")

    if startbtn:

        with start:

            with sr.Microphone() as source:

                with st.spinner(f"Recording for {duration} seconds..."):

                    audio = r.listen(source, phrase_time_limit=duration)
                    time.sleep(duration)

            try:
                text = r.recognize_google(audio)
                st.session_state.audio_text = text
                st.success("Recognized Text")
            except:
                st.error("Sorry, I did not understand the audio")
    # -----------------------------
    # PROCESS QUERY
    # -----------------------------
    if processbtn:
        with process:
            if not st.session_state.document_ready:
                st.warning("Please process a document first")

            elif st.session_state.audio_text is None:
                st.warning("Please record a question first")

            else:
                with st.spinner("Generating response..."):
                    response, relevant_chunks = app.ask_question(
                        st.session_state.audio_text
                    )

                    st.session_state.response = response

                st.subheader("Response")
                st.write(response)
                print(relevant_chunks)
            
                # Saving voice file in mp3
                engine.save_to_file(response, 'response.mp3')
                engine.runAndWait()
                
                audio_file = open('response.mp3', 'rb')
                audio_bytes = audio_file.read()
                
                st.audio(audio_bytes, format="audio/mp3")
                