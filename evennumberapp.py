# evennumberapp.py - Streamlit Application for Even/Odd Prediction and Translation

import streamlit as st
from gtts import gTTS # Used for Text-to-Speech
import base64
# No longer importing googletrans as gTTS is used for voice, and translations are pre-defined.
# No longer importing random as the random number generator feature was removed.

# --- Page Setup ---
st.set_page_config(page_title="Even or Odd Game 🎮", page_icon="🎲")

# --- Custom CSS matching your login app colors ---
def apply_custom_styling():
    custom_css = """
    <style>
    /* Main app background - dark navy like your login app */
    .main {
        background-color: #0f172a; /* Adjusted to match primary_bg from login app */
        color: #f8fafc; /* text_primary */
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp > header {
        background-color: #1e293b; /* secondary_bg */
        border-bottom: 1px solid #334155;
    }
    .stSidebar {
        background-color: #1e293b; /* secondary_bg */
        padding-top: 2rem;
    }
    .stSidebar .stRadio > label {
        color: #f8fafc; /* text_primary */
        font-weight: bold;
    }
    .stSidebar .stRadio div[role="radiogroup"] label {
        color: #94a3b8; /* text_secondary */
    }
    .stSidebar .stRadio div[role="radiogroup"] label:hover {
        color: #3b82f6; /* primary_blue */
    }
    .stButton > button {
        background-color: #3b82f6; /* primary_blue */
        color: #f8fafc; /* text_primary */
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #2563eb; /* Darker blue on hover */
    }
    .stTextInput > div > div > input {
        background-color: #334155; /* card_bg */
        color: #f8fafc; /* text_primary */
        border: 1px solid #64748b; /* text_muted */
        border-radius: 8px;
        padding: 10px;
    }
    .stTextInput > label {
        color: #f8fafc; /* text_primary */
        font-weight: bold;
    }
    .stAlert {
        border-radius: 8px;
    }
    .stAlert.success {
        background-color: #10b98120; /* success_green with transparency */
        color: #10b981;
    }
    .stAlert.error {
        background-color: #ef444420; /* danger_red with transparency */
        color: #ef4444;
    }
    .stAlert.warning {
        background-color: #f59e0b20; /* gold_accent with transparency */
        color: #f59e0b;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc; /* text_primary */
    }
    
    /* Specific overrides for your previous CSS that might conflict */
    /* Ensure .stApp background is consistent */
    .stApp {
        background-color: #0f172a; /* Ensure this is the main background */
    }
    /* Adjusting sidebar background if it was too light */
    .css-1d391kg, .css-1lcbmhc { /* These classes might change with Streamlit versions */
        background-color: #1e293b !important; /* secondary_bg */
    }
    /* Adjusting button hover colors to match your theme */
    .stButton > button:hover {
        background-color: #2563eb !important; /* Darker primary_blue */
    }
    /* Adjusting alert colors to match your theme */
    .stSuccess {
        background-color: rgba(16, 185, 129, 0.1) !important; /* success_green with transparency */
        border-left: 4px solid #10b981 !important; /* success_green */
    }
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important; /* danger_red with transparency */
        border-left: 4px solid #ef4444 !important; /* danger_red */
    }
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important; /* gold_accent with transparency */
        border-left: 4px solid #f59e0b !important; /* gold_accent */
    }
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1) !important; /* primary_blue with transparency */
        border-left: 4px solid #3b82f6 !important; /* primary_blue */
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Apply the custom styling
apply_custom_styling()

# --- Language options and translations ---
language_data = {
    "English 🇬🇧": {
        "code": "en",
        "title": "🔢 Even or Odd Fun Game for Kids!",
        "subtitle": "Learn numbers and languages with sound and smiles 😊",
        "name_prompt": "🧒 What is your name?",
        "number_prompt": "🔢 Type any number:",
        "play_button": "🔊 Play Voice",
        "even_result": lambda num, name: f"{num} is an even number, {name}! 🎉",
        "odd_result": lambda num, name: f"{num} is an odd number, {name}! 🎉",
        "even_info": "✅ An even number is divisible by 2. Example: 2, 4, 6...",
        "odd_info": "🧐 An odd number is NOT divisible by 2. Example: 1, 3, 5...",
        "error_msg": "🚫 Please enter a valid whole number.",
        "audio_error": "⚠️ Oops! Could not play audio."
    },
    "French 🇫🇷": {
        "code": "fr",
        "title": "🔢 Jeu Pair ou Impair pour Enfants!",
        "subtitle": "Apprenez les nombres et les langues avec du son et des sourires 😊",
        "name_prompt": "🧒 Quel est votre nom?",
        "number_prompt": "🔢 Tapez n'importe quel nombre:",
        "play_button": "🔊 Jouer la Voix",
        "even_result": lambda num, name: f"{num} est un nombre pair, {name}! 🎈",
        "odd_result": lambda num, name: f"{num} est un nombre impair, {name}! 🎈",
        "even_info": "✅ Un nombre pair est divisible par 2. Exemple: 2, 4, 6...",
        "odd_info": "🧐 Un nombre impair N'est PAS divisible par 2. Exemple: 1, 3, 5...",
        "error_msg": "🚫 Veuillez entrer un nombre entier valide.",
        "audio_error": "⚠️ Oups! Impossible de lire l'audio."
    },
    "Spanish 🇪🇸": {
        "code": "es",
        "title": "🔢 ¡Juego Par o Impar para Niños!",
        "subtitle": "Aprende números e idiomas con sonido y sonrisas 😊",
        "name_prompt": "🧒 ¿Cuál es tu nombre?",
        "number_prompt": "🔢 Escribe cualquier número:",
        "play_button": "🔊 Reproducir Voz",
        "even_result": lambda num, name: f"¡{num} es un número par, {name}! 🎊",
        "odd_result": lambda num, name: f"¡{num} es un número impar, {name}! 🎊",
        "even_info": "✅ Un número par es divisible por 2. Ejemplo: 2, 4, 6...",
        "odd_info": "🧐 Un número impar NO es divisible por 2. Ejemplo: 1, 3, 5...",
        "error_msg": "🚫 Por favor ingresa un número entero válido.",
        "audio_error": "⚠️ ¡Ups! No se pudo reproducir el audio."
    },
    "German 🇩🇪": {
        "code": "de",
        "title": "🔢 Gerade oder Ungerade Spiel für Kinder!",
        "subtitle": "Lerne Zahlen und Sprachen mit Klang und Lächeln 😊",
        "name_prompt": "🧒 Wie heißt du?",
        "number_prompt": "🔢 Gib eine beliebige Zahl ein:",
        "play_button": "🔊 Stimme Abspielen",
        "even_result": lambda num, name: f"{num} ist eine gerade Zahl, {name}! 🎪",
        "odd_result": lambda num, name: f"{num} ist eine ungerade Zahl, {name}! 🎪",
        "even_info": "✅ Eine gerade Zahl ist durch 2 teilbar. Beispiel: 2, 4, 6...",
        "odd_info": "🧐 Eine ungerade Zahl ist NICHT durch 2 teilbar. Beispiel: 1, 3, 5...",
        "error_msg": "🚫 Bitte gib eine gültige ganze Zahl ein.",
        "audio_error": "⚠️ Ups! Audio konnte nicht abgespielt werden."
    },
    "Italian 🇮🇹": {
        "code": "it",
        "title": "🔢 Gioco Pari o Dispari per Bambini!",
        "subtitle": "Impara numeri e lingue con suoni e sorrisi 😊",
        "name_prompt": "🧒 Qual è il tuo nome?",
        "number_prompt": "🔢 Scrivi qualsiasi numero:",
        "play_button": "🔊 Riproduci Voce",
        "even_result": lambda num, name: f"{num} è un numero pari, {name}! 🎨",
        "odd_result": lambda num, name: f"{num} è un numero dispari, {name}! 🎨",
        "even_info": "✅ Un numero pari è divisibile per 2. Esempio: 2, 4, 6...",
        "odd_info": "🧐 Un numero dispari NON è divisibile per 2. Esempio: 1, 3, 5...",
        "error_msg": "🚫 Inserisci un numero intero valido.",
        "audio_error": "⚠️ Ops! Impossibile riprodurre l'audio."
    }
}

# --- Sidebar for language selection ---
st.sidebar.markdown("<h2 style='color: #4A90E2; text-align: center;'>🌍 Select Language</h2>", unsafe_allow_html=True)

# FIX: Added a non-empty label and hid it using label_visibility
selected_language = st.sidebar.radio(
    "Choose Language for App Content:", # Non-empty label
    options=list(language_data.keys()),
    index=0,
    label_visibility="hidden" # Hides the label visually
)

# Get current language data
current_lang = language_data[selected_language]

# --- Title in selected language ---
st.markdown(f"<h1 style='text-align: center; color: white;'>{current_lang['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; color: #FFC107;'>{current_lang['subtitle']}</h4>", unsafe_allow_html=True)

# --- Inputs in selected language ---
st.markdown("---")
name = st.text_input(current_lang["name_prompt"])
number_input = st.text_input(current_lang["number_prompt"])

# --- Voice generation function ---
def generate_audio_and_play(sentence, language_code):
    try:
        tts = gTTS(text=sentence, lang=language_code)
        tts.save("result.mp3")
        audio_bytes = open("result.mp3", "rb").read()
        st.audio(audio_bytes, format="audio/mp3")
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f'<a href="data:audio/mp3;base64,{b64}" download="result.mp3">📥 Download Audio</a>', unsafe_allow_html=True)
    except Exception as e:
        st.error(current_lang["audio_error"])
        st.exception(e) # Display full exception for debugging

# --- Main Logic ---
if name and number_input:
    try:
        num = int(number_input)
        is_even = (num % 2 == 0)
        
        st.markdown("---")
        
        # Display result in selected language
        if is_even:
            result_text = current_lang["even_result"](num, name)
            info_text = current_lang["even_info"]
        else:
            result_text = current_lang["odd_result"](num, name)
            info_text = current_lang["odd_info"]
        
        st.success(result_text)
        
        # Play voice button in selected language
        if st.button(current_lang["play_button"]):
            generate_audio_and_play(result_text, current_lang["code"])
        
        st.info(info_text)

    except ValueError:
        st.error(current_lang["error_msg"])

# --- Sidebar info ---
st.sidebar.markdown("---")
st.sidebar.markdown("<h4 style='color: #FFC107;'>ℹ️ How to use:</h4>", unsafe_allow_html=True)
st.sidebar.markdown("1. Select your language", unsafe_allow_html=True)
st.sidebar.markdown("2. Enter your name", unsafe_allow_html=True)
st.sidebar.markdown("3. Type any number", unsafe_allow_html=True)
st.sidebar.markdown("4. Click play to hear the result!", unsafe_allow_html=True)
