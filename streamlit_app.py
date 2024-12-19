import streamlit as st
import speech_recognition as spr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import io

def initialize_pygame():
    pygame.mixer.init()

def recognize_speech(recog, source):
    try:
        recog.adjust_for_ambient_noise(source, duration=10)
        audio = recog.listen(source)
        recognized_text = recog.recognize_google(audio)
        return recognized_text.lower()
    except spr.UnknownValueError:
        st.error("Google Speech Recognition could not understand the audio.")
        return None
    except spr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_text(text, from_lang, to_lang):
    try:
        translator = Translator()
        translated = translator.translate(text, src=from_lang, dest=to_lang)
        return translated.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")
        return None

def main():
    st.title("🌐 AIYOU Translation App")
    
    # Prepare language lists
    language_list = sorted(list(LANGUAGES.values()))
    language_dict = {lang: code for code, lang in LANGUAGES.items()}
    
    # Sidebar for language selection
    st.sidebar.header("🔤 Language Settings")
    from_lang_name = st.sidebar.selectbox("Source Language", language_list, index=language_list.index('telugu'))
    to_lang_name = st.sidebar.selectbox("Target Language", language_list, index=language_list.index('english'))
    
    # Convert language names to codes
    from_lang_code = language_dict[from_lang_name]
    to_lang_code = language_dict[to_lang_name]
    
    # Speech Recognition Section
    st.header("🎙️ Speech Translation")
    
    # Initialize speech recognizer
    recog1 = spr.Recognizer()
    mc = spr.Microphone()
    
    # Speech Recording Button
    if st.button("🔴 Record Speech"):
        with mc as source:
            st.info("Speak now...")
            try:
                # Listen and recognize speech
                audio = recog1.listen(source)
                recognized_text = recog1.recognize_google(audio)
                
                # Display recognized text
                st.write("Recognized Text:", recognized_text)
                
                # Translate recognized text
                translated_text = translate_text(
                    recognized_text, 
                    from_lang_code, 
                    to_lang_code
                )
                
                if translated_text:
                    # Display translated text
                    st.success(f"Translated Text: {translated_text}")
                    
                    # Text to Speech
                    audio_data = text_to_speech(translated_text, to_lang_code)
                    
                    if audio_data:
                        # Play translated audio
                        initialize_pygame()
                        pygame.mixer.music.load(audio_data)
                        pygame.mixer.music.play()
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
    # Manual Translation Section
    st.header("✍️ Manual Translation")
    manual_text = st.text_input("Enter text to translate")
    
    if st.button("Translate Text"):
        if manual_text:
            # Translate manually entered text
            translated_text = translate_text(
                manual_text, 
                from_lang_code, 
                to_lang_code
            )
            
            if translated_text:
                # Display translated text
                st.success(f"Translated Text: {translated_text}")
                
                # Text to Speech
                audio_data = text_to_speech(translated_text, to_lang_code)
                
                if audio_data:
                    # Play translated audio
                    initialize_pygame()
                    pygame.mixer.music.load(audio_data)
                    pygame.mixer.music.play()
    
    # Available Languages Section
    st.header("🌍 Available Languages")
    st.write("Total Available Languages:", len(language_list))
    
    # Optional: Expandable list of languages
    with st.expander("View All Languages"):
        st.table({
            "Language": language_list,
            "Code": [language_dict[lang] for lang in language_list]
        })

if __name__ == "__main__":
    main()
