import streamlit as st
import os
import pandas as pd
import smtplib
import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="glowai", page_icon="💖", layout="wide")

# --- CZYSZCZENIE I BEZPIECZNY ZAPIS STYLU CSS ---
css_style = (
    "<style>"
    ".stApp { background-color: #fff9f6; }"
    "html, body, [class*='css'] { font-family: 'Montserrat', sans-serif; color: #2b2b2b; }"
    ".bg-huge-text { font-family: 'Cinzel', serif; font-size: 150px; color: rgba(224, 164, 164, 0.15); font-weight: 700; text-align: center; position: absolute; width: 100%; top: -40px; z-index: 0; pointer-events: none; letter-spacing: -5px; }"
    ".nav-bar { text-align: center; padding: 15px; font-size: 13px; letter-spacing: 2px; text-transform: uppercase; color: #a38585; border-bottom: 1px solid rgba(163, 133, 133, 0.15); margin-bottom: 30px; }"
    ".brand-title { font-family: 'Cinzel', serif; color: #c98a8a; font-size: 70px; text-align: center; font-weight: 600; letter-spacing: 4px; margin-top: 20px; }"
    ".brand-subtitle { text-align: center; color: #635252; font-size: 16px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 50px; }"
    ".skincare-card { background-color: #ffffff; padding: 40px; border-radius: 40px 0px 40px 0px; border: 1px solid #f7dede; box-shadow: 15px 15px 0px #f0cfcf; margin-bottom: 40px; position: relative; z-index: 1; }"
    ".gallery-img { border-radius: 20px; object-fit: cover; box-shadow: 0px 10px 25px rgba(201, 138, 138, 0.15); transition: transform 0.3s ease; }"
    ".gallery-img:hover { transform: scale(1.02); }"
    ".product-pill { background-color: #f7dede; color: #635252; padding: 20px; border-radius: 20px; margin-bottom: 15px; border: 1px solid #ebc5c5; }"
    "div.stButton > button:first-child { background-color: #c98a8a !important; color: white !important; border-radius: 30px !important; border: none !important; padding: 15px 40px !important; font-size: 16px !important; font-weight: 600 !important; letter-spacing: 2px !important; width: 100%; box-shadow: 0px 8px 20px rgba(201, 138, 138, 0.3) !important; }"
    "div.stButton > button:first-child:hover { background-color: #b87676 !important; transform: translateY(-2px); }"
    "</style>"
)

st.markdown(css_style, unsafe_allowed_html=True)

# --- WYSTAWKA FRONTENDU ---
st.markdown('<div class="nav-bar">About us &nbsp; • &nbsp; Catalog &nbsp; • &nbsp; Skincare &nbsp; • &nbsp; AI Consultant</div>', unsafe_allowed_html=True)
st.markdown('<div class="bg-huge-text">GLOW</div>', unsafe_allowed_html=True)
st.markdown('<div class="brand-title">rhode x glowai</div>', unsafe_allowed_html=True)
st.markdown('<div class="brand-subtitle">New philosophy of selfcare: healthy skin first</div>', unsafe_allowed_html=True)

col_img1, col_img2, col_img3 = st.columns(3)
with col_img1:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=500" width="100%">', unsafe_allowed_html=True)
with col_img2:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1556229174-5e42a09e45af?q=80&w=500" width="100%">', unsafe_allowed_html=True)
with col_img3:
    st.markdown('<img class="gallery-img" src="https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?q=80&w=500" width="100%">', unsafe_allowed_html=True)

st.markdown("<br><br>", unsafe_allowed_html=True)

st.markdown('<div class="skincare-card">', unsafe_allowed_html=True)
st.markdown("<h2 style='font-family: serif; color: #635252; text-align:center;'>🌸 Spersonalizowany Konsultant AI</h2>", unsafe_allowed_html=True)

user_input = st.text_area("Opisz swoją skórę (np. 'mam problem z egzemą i suchą skórą'):", placeholder="Napisz to w 100% naturalnie...")
user_email = st.text_input("Twój e-mail, na który wyślemy oficjalny raport:", placeholder="your.email@gmail.com")

generate_btn = st.button("ANALIZUJ PROFIL SKÓRY ✨")
st.markdown('</div>', unsafe_allowed_html=True)

# --- CONFIG ---
GROQ_API_KEY = "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"
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"

def send_email(receiver_email, content):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = "🌸 Twój Osobisty Plan Pielęgnacyjny od GlowAI"
        msg.attach(MIMEText(content, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return "Raport wysłany na Twojego maila!"
    except Exception as e:
        return f"Błąd poczty: {e}"

def symuluj_agentow_ai_native(opis_skory):
    url = "https://api.groq.com/openai/v1/chat/completions"
    system_prompt = """Jesteś zaawansowanym systemem kosmetologicznym działającym jako zespół 5 agentów: Dermatolog, Technolog, Strateg, Redaktor i Spedytor.
    Przeanalizuj opis skóry pacjenta. Postaw krótką diagnozę (Dermatolog), dobierz pasujący składnik aktywny i wyszukaj przykładowy produkt w bazie (Technolog), oceń opłacalność (Strateg) i sformatuj całość w przepiękny, przyjacielski, dziewczęcy, ale profesjonalny raport po polsku (Redaktor). Nie używaj żadnego kodu ani znaczników technicznych."""
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Opis skóry pacjenta: {opis_skory}"}
        ],
        "temperature": 0.3
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {GROQ_API_KEY}')
    
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['choices'][0]['message']['content']

if generate_btn:
    if not user_input or not user_email or "@" not in user_email:
        st.error("💖 Słońce, podaj poprawny opis cery oraz swój adres e-mail!")
    else:
        with st.spinner("✨ Nasz inteligentny system analizuje Twój profil skóry..."):
            try:
                wynik = symuluj_agentow_ai_native(user_input)
                status_maila = send_email(user_email, wynik)
                
                st.balloons()
                st.success(f"💖 {status_maila}")
                
                st.markdown("### 📋 Wynik analizy kosmetologicznej:")
                st.info(wynik)
                
                st.markdown("### 🧴 Wyselekcjonowane produkty dla Ciebie:")
                st.markdown("""
                    <div class="product-pill">
                        <b>🎀 Rhode Fluid Nawilżający</b> — Intensywne wsparcie bariery hydrolipidowej.
                    </div>
                    <div class="product-pill">
                        <b>🌿 Sage Pure Barrier Cream</b> — Łagodzenie podrażnień i głęboka regeneracja suchej skóry.
                    </div>
                """, unsafe_allowed_html=True)
                
            except Exception as e:
                st.error(f"Wystąpił problem. Szczegóły: {e}")
