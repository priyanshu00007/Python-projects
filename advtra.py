import streamlit as st
import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            st.error("Speech recognition failed")

def main():
    st.title("Voice-to-Text")
    st.write("Click the button to start speaking")

    if st.button("Listen"):
        text = listen()
        st.write("Recognized Text:")
        st.code(text)

if __name__ == "__main__":
    main()