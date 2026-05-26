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
.csv-ingredients { font-size: 12px; color: #38242C; margin-top: 10px; line-height: 1.5; }

/* Stopka */
.footer {
    text-align: center;
    font-size: 11px;
    letter-spacing: 3px;
    color: #C27F97;
    margin-top: 80px;
    border-top: 1px solid #D8AAB7;
    padding-top: 30px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- FUNKCJA BEZPIECZNYCH ZDJĘĆ Z ESTETYCZNYM ZASTĘPSTWEM ---
def safe_image(img_name):
    try:
        # Streamlit natywnie próbuje załadować plik
        st.image(img_name, use_container_width=True)
    except Exception:
        # Jeśli pliku nie ma, ładujemy śliczny różowy kafelek zamiast brzydkiego błędu/psa
        st.markdown(
            f"<div style='height: 250px; background-color: #D8AAB7; border: 2px solid #C27F97; "
            f"border-radius: 12px; display: flex; align-items: center; justify-content: center; "
            f"color: #6B2F4A; font-weight: 600; font-size: 12px; text-align: center; margin-bottom: 1rem;'>"
            f"Miejsce na zdjęcie<br>🤍✨</div>", 
            unsafe_allow_html=True
        )

# --- UKŁAD KOLUMN ---
col_left, col_center, col_right = st.columns([1, 2.2, 1], gap="large")

# LEWA KOLUMNA
with col_left:
    st.write("")
    safe_image("1fa08f5d77417f45981c55e8b887f909.jpg")
    safe_image("102e80d2a00f1417283bfd743d021a76.jpg")
    safe_image("9438d31b27d424e2feb4e744c7578aa3.jpg")

# PRAWA KOLUMNA
with col_right:
    st.write("")
    safe_image("700129929a2803b16ab124197ec8ba69.jpg")
    safe_image("daa4eaf344eebaaa5d8e72625ca7f976.jpg")
    safe_image("edf73f24d9d6a298f7d0626c20569a7c.jpg")

# ŚRODKOWA KOLUMNA (GŁÓWNA)
with col_center:
    # GIGANTYCZNE LOGO
    st.markdown('<div class="huge-logo">GLOW.AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your digital skincare confidant</div>', unsafe_allow_html=True)
    
    # Inputy profilu
    c1, c2 = st.columns(2)
    with c1:
        user_name = st.text_input("Name", placeholder="TWOJE IMIĘ", label_visibility="collapsed")
    with c2:
        user_email = st.text_input("Email", placeholder="TWÓJ EMAIL", label_visibility="collapsed")
    
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # Inicjalizacja wiadomości w czacie
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Cześć piękna! 🤍 Gotowa zromantyzować swoją rutynę pielęgnacyjną? Zdradź mi, czego dzisiaj pragnie Twoja skóra."}
        ]

    # Wyświetlanie czatu (z naszymi awatarami)
    for message in st.session_state.messages:
        avatar_icon = "🤍" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # Wp
