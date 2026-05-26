import streamlit as st
import os
import time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI", page_icon="🎀", layout="wide")

# --- BEZWZGLĘDNA PALETA KOLORÓW I CSS ---
css_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;800&display=swap');

/* Tło aplikacji: #F5ECEE */
.stApp, .main, [data-testid="stAppViewContainer"] {
    background-color: #F5ECEE !important;
}

/* Tekst i czcionka: #38242C */
html, body, p, div, span, h1, h2, h3, input, textarea {
    font-family: 'Montserrat', sans-serif !important;
    color: #38242C !important;
}

div[data-testid="stAppViewBlockContainer"] {
    padding-top: 1rem !important;
}

/* LOGO NA SAMEJ GÓRZE (#6B2F4A) */
.huge-logo {
    font-size: 80px !important;
    font-weight: 800 !important;
    text-align: center !important;
    letter-spacing: 15px !important;
    color: #6B2F4A !important;
    margin-top: 0px !important;
    margin-bottom: 15px !important;
    line-height: 1 !important;
}
.subtitle {
    font-size: 14px !important;
    text-align: center !important;
    letter-spacing: 6px !important;
    text-transform: uppercase !important;
    color: #A24D72 !important;
    margin-bottom: 40px !important;
    font-weight: 600 !important;
}

/* ZDJĘCIA PO BOKACH (#C27F97) */
[data-testid='stImage'] img {
    border-radius: 12px !important;
    object-fit: cover;
    border: 2px solid #C27F97 !important;
    box-shadow: 0px 8px 20px rgba(107, 47, 74, 0.1) !important;
    margin-bottom: 15px !important;
}

/* POLA TEKSTOWE PROFILU I WYSZUKIWARKI (#F5ECEE i #C27F97) */
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
    letter-spacing: 1px;
    font-size: 11px;
    font-weight: 600;
}

/* DYMKI CZATU (#F5ECEE i #D8AAB7) */
[data-testid="stChatMessage"] {
    background-color: #F5ECEE !important;
    border-radius: 16px !important;
    border: 2px solid #D8AAB7 !important;
    padding: 15px !important;
    margin-bottom: 15px !important;
    font-size: 14px !important;
}
[data-testid="stChatMessage"]:nth-child(even) {
    background-color: #D8AAB7 !important;
    border: 2px solid #C27F97 !important;
}

/* =========================================================
   OSTATECZNA BLOKADA CZERNI W PASKU CZATU I PRZYCISKU
   ========================================================= */

/* Główny pasek */
div[data-testid="stChatInput"] {
    background-color: #F5ECEE !important;
    border: 2px solid #C27F97 !important;
    border-radius: 30px !important;
    padding: 4px 10px !important;
}
div[data-testid="stChatInput"]:focus-within {
    border: 2px solid #A24D72 !important;
}

/* Zmuszamy Streamlita, by nie podmieniał tła w środku na czarne */
div[data-testid="stChatInput"] > div, 
div[data-testid="stChatInput"] * {
    background-color: transparent !important;
}

/* Wymuszenie CIEMNEGO tekstu w trakcie pisania */
div[data-testid="stChatInput"] textarea {
    color: #38242C !important; 
    -webkit-text-fill-color: #38242C !important;
    caret-color: #A24D72 !important; 
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #C27F97 !important;
    -webkit-text-fill-color: #C27F97 !important;
}

/* MORDERCA CZARNEGO PRZYCISKU (Identyfikator docelowy Streamlita) */
button[data-testid="stChatInputSubmitButton"],
button[data-testid="stChatInputSubmitButton"]:enabled,
button[data-testid="stChatInputSubmitButton"]:disabled,
button[data-testid="stChatInputSubmitButton"]:focus,
button[data-testid="stChatInputSubmitButton"]:active {
    background-color: #A24D72 !important;
    background: #A24D72 !important; 
    border-radius: 50% !important;
    border: none !important;
    box-shadow: none !important;
    opacity: 1 !important;
}

/* Efekt najechania myszką */
button[data-testid="stChatInputSubmitButton"]:hover {
    background-color: #6B2F4A !important;
    background: #6B2F4A !important;
}

/* Ikona strzałki - wymuszenie jasnego koloru #F5ECEE */
button[data-testid="stChatInputSubmitButton"] svg,
button[data-testid="stChatInputSubmitButton"] path {
    fill: #F5ECEE !important;
    color: #F5ECEE !important;
    stroke: transparent !important;
}


/* PRZYCISK MAILOWY (#A24D72) */
div.stButton > button:first-child {
    background-color: #A24D72 !important;
    color: #F5ECEE !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 15px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    margin-top: 10px !important;
}
div.stButton > button:first-child:hover {
    background-color: #6B2F4A !important;
}

/* WYSZUKIWARKA CSV WYNIKI */
.csv-result {
    background-color: #F5ECEE;
    border: 2px solid #D8AAB7;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
}
.csv-brand { font-weight: 800; color: #6B2F4A; font-size: 14px; text-transform: uppercase; }
.csv-name { font-weight: 600; color: #A24D72; font-size: 13px; }
.csv-ingredients { font-size: 11px; color: #38242C; margin-top: 8px; }

/* STOPKA (#C27F97) */
.footer {
    text-align: center;
    font-size: 11px;
    letter-spacing: 3px;
    color: #C27F97;
    margin-top: 60px;
    border-top: 1px solid #D8AAB7;
    padding-top: 20px;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- FUNKCJA WYSYŁKI MAILA ---
def send_email_report(receiver_email, name, transcript):
    try:
        msg = MIMEMultipart()
        msg['From'] = "n.zudzin@gmail.com"
        msg['To'] = receiver_email
        msg['Subject'] = f"🎀 Twój plan pielęgnacyjny GlowAI — Witaj {name}!"
        body = f"Cześć {name}!\n\nOto zapis z Twojej konsultacji:\n\n{transcript}\n\nStay glowing, XOXO!"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("n.zudzin@gmail.com", "syry wcts pymb yscg")
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False

# --- FUNKCJA ZDJĘĆ Z RÓŻOWYM KAFELKIEM ZASTĘPCZYM ---
def safe_image(img_name):
    try:
        st.image(img_name, use_container_width=True)
    except Exception:
        st.markdown(
            f"<div style='height: 200px; background-color: #D8AAB7; border: 2px solid #C27F97; "
            f"border-radius: 12px; display: flex; align-items: center; justify-content: center; "
            f"color: #6B2F4A; font-weight: 600; font-size: 12px; margin-bottom: 15px;'>"
            f"Miejsce na zdjęcie 🤍</div>", unsafe_allow_html=True)

# =====================================================================
# GŁÓWNY UKŁAD STRONY
# =====================================================================

# 1. LOGO NA SAMEJ GÓRZE STRONY (Pełna szerokość)
st.markdown('<div class="huge-logo">GLOW.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your digital skincare confidant</div>', unsafe_allow_html=True)

# 2. PODZIAŁ NA 3 KOLUMNY (Boki: zdjęcia, Środek: funkcje)
col_left, col_center, col_right = st.columns([1, 2.2, 1], gap="large")

with col_left:
    safe_image("1fa08f5d77417f45981c55e8b887f909.jpg")
    safe_image("102e80d2a00f1417283bfd743d021a76.jpg")
    safe_image("9438d31b27d424e2feb4e744c7578aa3.jpg")

with col_right:
    safe_image("700129929a2803b16ab124197ec8ba69.jpg")
    safe_image("daa4eaf344eebaaa5d8e72625ca7f976.jpg")
    safe_image("edf73f24d9d6a298f7d0626c20569a7c.jpg")

# --- ŚRODKOWA KOLUMNA (CZAT, WYSZUKIWARKA, MAIL) ---
with col_center:
    
    # PROFIL
    c1, c2 = st.columns(2)
    with c1:
        user_name = st.text_input("Name", placeholder="TWOJE IMIĘ", label_visibility="collapsed")
    with c2:
        user_email = st.text_input("Email", placeholder="TWÓJ EMAIL", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # CZAT KOSMETOLOGICZNY
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Cześć piękna! 🤍 Gotowa zromantyzować swoją rutynę pielęgnacyjną? Zdradź mi, czego dzisiaj pragnie Twoja skóra."}
        ]

    for message in st.session_state.messages:
        avatar_icon = "🤍" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    if prompt := st.chat_input("Zdradź mi sekrety swojej skóry..."):
        with st.chat_message("user", avatar="🤍"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Analizuję Twój profil glow... ✨"):
                time.sleep(1.5) 
                mock_response = (
                    "Wiem dokładnie, co tu się dzieje! ✨ Twoja bariera hydrolipidowa potrzebuje odrobiny miłości.\n\n"
                    "**Diagnoza:** Odwodnienie połączone z lekkim podrażnieniem.\n\n"
                    "**Protokół:** Przejdź na mleczną emulsję, zalej skórę Ceramidami (polecam poszukać hasła 'Serum' w naszej bazie niżej) i domknij to kremem peptydowym. Keep glowing! 🧴🤍"
                )
                st.markdown(mock_response)
        st.session_state.messages.append({"role": "assistant", "content": mock_response})

    # WYSZUKIWARKA KOSMETYKÓW
    st.markdown("<br><div style='border-top: 2px solid #D8AAB7; margin: 20px 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #6B2F4A; font-size: 16px; letter-spacing: 2px; font-weight: 800;'>🔍 BAZA SKŁADNIKÓW GLOWAI</h3>", unsafe_allow_html=True)
    
    search_query = st.text_input("Szukaj", placeholder="Wpisz kosmetyk (np. Serum, Cream)...", label_visibility="collapsed")
    
    if search_query:
        try:
            df = pd.read_csv('cosmetics.csv')
            mask = df['Name'].str.contains(search_query, case=False, na=False) | df['Brand'].str.contains(search_query, case=False, na=False)
            results = df[mask].head(2) 
            
            if not results.empty:
                for idx, row in results.iterrows():
                    cena = f"${row['Price']}" if 'Price' in row and pd.notna(row['Price']) else "Brak ceny"
                    sklad = row['Ingredients'] if 'Ingredients' in row and pd.notna(row['Ingredients']) else "Utajniony"
                    st.markdown(
                        f"<div class='csv-result'>"
                        f"<div class='csv-brand'>{row['Brand']}</div>"
                        f"<div class='csv-name'>{row['Name']} | {cena}</div>"
                        f"<div class='csv-ingredients'><b>INCI:</b> {sklad}</div>"
                        f"</div>", unsafe_allow_html=True)
            else:
                st.warning("Nie znaleziono produktu. ✨", icon="🤍")
        except Exception:
            st.error("Brak pliku cosmetics.csv w systemie!", icon="🚨")

    # PRZYCISK MAILOWY NA SAMYM DOLE ŚRODKA
    st.markdown("<div style='border-top: 2px solid #D8AAB7; margin: 20px 0;'></div>", unsafe_allow_html=True)
    if st.button("WYŚLIJ ANALIZĘ NA MÓJ EMAIL 🕊️"):
        if not user_email or "@" not in user_email:
            st.error("Wpisz poprawny e-mail u góry! ✨", icon="🤍")
        elif len(st.session_state.messages) < 2:
            st.warning("Najpierw opisz swój problem na czacie!", icon="🤍")
        else:
            with st.spinner("Wysyłam raport..."):
                full_transcript = "\n\n".join([f"{'Ty' if m['role']=='user' else 'GlowAI'}: {m['content']}" for m in st.session_state.messages])
                if send_email_report(user_email, user_name, full_transcript):
                    st.success("Sprawdź skrzynkę! 🤍", icon="✨")
                else:
                    st.error("Błąd serwera poczty.", icon="🚨")

# 3. STOPKA NA DOLE STRONY
st.markdown('<div class="footer">New philosophy of selfcare: healthy skin first</div>', unsafe_allow_html=True)
