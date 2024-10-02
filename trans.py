import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os
from io import BytesIO

# Initialize the translator
translator = Translator()

# Function to get available languages
def get_languages():
    return {
        'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic', 'hy': 'Armenian', 'bn': 'Bengali', 
        'ca': 'Catalan', 'zh': 'Chinese', 'zh-cn': 'Chinese (Mandarin/China)', 
        'zh-tw': 'Chinese (Mandarin/Taiwan)', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish', 
        'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'fi': 'Finnish', 'fr': 'French', 
        'de': 'German', 'el': 'Greek', 'hi': 'Hindi', 'hu': 'Hungarian',"Gujarati": "gu", 'is': 'Icelandic', 
        'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'km': 'Khmer (Cambodian)', "Marathi": "mr", 
        'ko': 'Korean', 'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian', 'no': 'Norwegian', 
        'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sr': 'Serbian', 
        'si': 'Sinhala', 'sk': 'Slovak', 'es': 'Spanish', 'sw': 'Swahili', 'sv': 'Swedish', 
        'ta': 'Tamil', 'th': 'Thai', 'tr': 'Turkish', 'uk': 'Ukrainian', 'vi': 'Vietnamese'
    }

# Function to translate text
def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        return str(e)

# Function to convert text to speech
def text_to_speech(text, lang, voice):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp
    except Exception as e:
        return str(e)

# Streamlit app
def main():
    st.title("Language Translator and Text-to-Speech App")

    # Input text
    input_text = st.text_area("Enter text to translate:", height=150)

    # Get available languages
    languages = get_languages()

    # Select target language
    target_lang = st.selectbox("Select target language:", list(languages.values()))

    # Get the language code
    target_lang_code = list(languages.keys())[list(languages.values()).index(target_lang)]

    # Translate button
    if st.button("Translate"):
        if input_text:
            translation = translate_text(input_text, target_lang_code)
            st.write("Translation:")
            st.write(translation)

            # Text-to-speech
            st.write("Text-to-Speech:")
            
            # Voice selection (Note: This is a simplified version, actual voice options may vary)
            voice = st.selectbox("Select voice:", ["Default", "Male", "Female"])
            
            audio_fp = text_to_speech(translation, target_lang_code, voice)
            
            if isinstance(audio_fp, BytesIO):
                st.audio(audio_fp, format='audio/mp3')
            else:
                st.error(f"Error in text-to-speech conversion: {audio_fp}")
        else:
            st.warning("Please enter some text to translate.")

if __name__ == "__main__":
    main()