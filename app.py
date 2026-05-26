import streamlit as st
import os
import time
import pandas as pd

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI", page_icon="🎀", layout="wide")

# --- EDGY & CLEAN GIRL UI (BEZWZGLĘDNA PALETA KOLORÓW) ---
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;800&display=swap');

/* Tło całej aplikacji - jasny róż #F5ECEE */
.stApp, .main, [data-testid="stAppViewContainer"] {
    background-color: #F5ECEE !important;
}

/* Wymuszenie fontu Montserrat dla całego tekstu oraz głównego koloru #38242C */
html, body, p, div, span, h1, h2, h3, input, textarea {
    font-family: 'Montserrat', sans-serif !important;
    color: #38242C !important;
}

/* Ukrycie marginesów górnych */
div[data-testid="stAppViewBlockContainer"] {
    padding-top: 2rem !important;
}

/* GIGANTYCZNE LOGO GLOW.AI (#6B2F4A) */
.huge-logo {
    font-size: 85px !important;
    font-weight: 800 !important;
    text-align: center !important;
    letter-spacing: 15px !important;
    color: #6B2F4A !important;
    margin-top: 10px !important;
    margin-bottom: -15px !important;
    line-height: 1 !important;
}

/* Subtitle (#A24D72) */
.subtitle {
    font-size: 13px !important;
    text-align: center !important;
    letter-spacing: 6px !important;
    text-transform: uppercase !important;
    color: #A24D72 !important;
    margin-bottom: 60px !important;
    font-weight: 600 !important;
}

/* Zdjęcia po bokach z ramką #C27F97 */
[data-testid='stImage'] img {
    border-radius: 12px !important;
    object-fit: cover;
    border: 2px solid #C27F97 !important;
    box-shadow: 0px 10px 25px rgba(56, 36, 44, 0.1) !important;
}

/* Pola tekstowe - tło #F5ECEE, ramka #C27F97 */
div[data-baseweb="input"] > div {
    background-color: #F5ECEE !important;
    border: 2px solid #C27F97 !important;
    border-radius: 8px !important;
}
div[data-baseweb="input"] > div:focus-within {
    border: 2px solid #A24D72 !important;
}
input::placeholder {
    color: #C27F97 !important;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 600;
}

/* WYGLĄD DYMKÓW CZATU - Tło #F5ECEE, ramka #D8AAB7 */
[data-testid="stChatMessage"] {
    background-color: #F5ECEE !important;
    border-radius: 16px !important;
    border: 2px solid #D8AAB7 !important;
    padding: 15px !important;
    margin-bottom: 15px !important;
    font-size: 15px !important;
    box-shadow: none !important;
}
/* Dymek bota - ciemniejszy róż #D8AAB7 */
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #D8AAB7 !important;
    border: 2px solid #C27F97 !important;
}

/* Pasek wpisywania na dole */
div[data-testid="stChatInput"] {
    background-color: #F5ECEE !important;
    border: 2px solid #C27F97 !important;
    border-radius: 30px !important;
}

/* PRZYCISKI - Tło #A24D72 */
div.stButton > button:first-child {
    background-color: #A24D72 !important;
    color: #F5ECEE !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 15px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    width: 100% !important;
    margin-top: 10px !important;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    background-color: #6B2F4A !important;
    color: #F5ECEE !important;
    transform: translateY(-2px);
}

/* Estetyczna Karta Wyników Wyszukiwania CSV */
.csv-result {
    background-color: #F5ECEE;
    border: 2px solid #D8AAB7;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0px 5px 15px rgba(107, 47, 74, 0.05);
}
.csv-brand { font-weight: 800; color: #6B2F4A; font-size: 16px; text-transform: uppercase; letter-spacing: 1px; }
.csv-name { font-weight: 600; color: #A24D72; font-size: 14px; margin-bottom: 10px; }
.csv-ingredients { font-
