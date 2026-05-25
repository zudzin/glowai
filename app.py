import streamlit as st
import os
import pandas as pd
import smtplib
import json
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- USTAWIENIA STRONY ---
st.set_page_config(page_title="GlowAI x Gossip Girl", page_icon="💋", layout="wide")

# --- EDGY PINK & PLOTKARA VIBE DESIGN (CSS) ---
css_style = (
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&display=swap');"
    ".stApp { background-color: #fffaf7; }"
    "html, body, [class*='css'] { font-family: 'Montserrat', sans-serif; color: #2b2b2b; }"
    
    # Logo na samym górze
    ".brand-logo { font-family: 'Cinzel', serif; color: #c98a8a; font-size: 60px; text-align: center; font-weight: 700; letter-spacing: 6px; margin-top: 10px; margin-bottom: 5px; }"
    ".brand-tagline { text-align: center; color: #a38585; font-size: 13px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px; }"
    
    # Stylizacja karty profilu użytkownika
    ".profile-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #f7dede; box-shadow: 8px 8px 0px #f0cfcf; margin-bottom: 25px; }"
    
    # Personalizacja dymków czatu na różowo/kremowo
    "[data-testid='stChatMessage'] { background-color: #ffffff; border-radius: 20px; border: 1px solid #f7dede; margin-bottom: 10px; padding: 15px; }"
    "[data-testid='stChatMessage']:nth-child(even) { background-color: #fff0f1; border: 1px solid #ebc5c5; }"
    
    # Zdjęcia po bokach (Wymuszony styl dla st.image)
    "[data-testid='stImage'] img { border-radius: 15px; object-fit: cover; border: 1px solid #f7dede; box-shadow: 0px 4px 15px rgba(201,138,138,0.1); transition: transform 0.3s ease; }"
    "[data-testid='stImage'] img:hover { transform: scale(1.03); }"
    
    # Stopka na samym dole strony
    ".brand-footer { text-align: center; font-family: 'Cinzel', serif; color: #a38585; font-size: 16px; letter-spacing: 3px; text-transform: uppercase; margin-top: 60px; padding: 25px; border-top: 1px solid rgba(163, 133, 133, 0.15); }"
    
    # Przycisk wysyłki maila
    "div.stButton > button:first-child { background-color: #c98a8a !important; color: white !important; border-radius: 25px !important; border: none !important; padding: 10px 25px !important; font-size: 14px !important; font-weight: 600 !important; letter-spacing: 1px !important; width: 100%; box-shadow: 0px 4px 12px rgba(201, 138, 138, 0.2) !important; }"
    "div.stButton > button:first-child:hover { background-color: #b87676 !important; transform: translateY(-1px); }"
    "</style>"
)
st.markdown(css_style, unsafe_allow_html=True)

# --- POLA CONFIG DLA AI I POCZTY ---
GROQ_API_KEY = "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"
GMAIL_USER = "n.zudzin@gmail.com"
GMAIL_PASS = "syry wcts pymb yscg"

def send_email_transcript(receiver_email, name, transcript):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = f"💋 Transkrypcja Twojej konsultacji GlowAI — Witaj {name}!"
        
        body = f"Cześć {name}!\n\nOto pełna historia Twojej czatowej rozmowy z wirtualnymi agentami GlowAI:\n\n"
        body += transcript
        body += "\n\nStay glowing, XOXO!\nZespół GlowAI"
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return "Pełna historia rozmowy została wysłana na Twój e-mail! 💌"
    except Exception as e:
        return f"Błąd wysyłki raportu na e-mail: {e}"

def pytaj_agentow_czat(imie, historia, nowy_prom):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    system_prompt = (
        f"Jesteś zaawansowanym systemem kosmetologicznym GlowAI, składającym się z 5 wirtualnych agentów "
        f"(Dermatolog, Technolog, Strateg, Redaktor, Spedytor). Rozmawiasz z użytkownikiem o imieniu {imie} "
        f"w stylu 'Plotkary' (Gossip Girl vibe) — jesteś błyskotliwą, luksusową przyjaciółką, która wie wszystko o "
        f"sekretach skóry, piszesz z klasą, lekko edgy, używając emoji (np. 💋, 🌸, ✨, 🧴). W każdej odpowiedzi "
        f"zintegruj wiedzę biologiczną o skórze (Dermatolog), dobierz odpowiednie składniki aktywne z bazy (Technolog), "
        f"wspomnij żartobliwie o budżecie lub rynkowych cenach (Strateg) i sformatuj odpowiedź jako płynną, "
        f"przyjacielską wiadomość na Messengerze (Redaktor). Odpowiadaj wyłącznie po polsku."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in historia:
        messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})
    messages.append({"role": "user", "content": nowy_prom})
    
    data = {
        "model": "llama3-8b-8192",
        "messages": messages,
        "temperature": 0.4
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {GROQ_API_KEY}')
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res['choices'][0]['message']['content']
    except Exception as e:
        return f"💋 Ojej, moje serwery na chwilę straciły zasięg! Szczegóły: {e}"

# --- UKŁAD STRONY: 3 KOLUMNY ---
col_left, col_center, col_right = st.columns([1, 2, 1])

def wyswietl_zdjecie_bezpiecznie(nazwa_pliku, url_zastepczy):
    # Bezpieczne ładowanie pliku za pomocą natywnej funkcji Streamlit (st.image)
    if os.path.exists(nazwa_pliku):
        st.image(nazwa_pliku, use_container_width=True)
    else:
        st.image(url_zastepczy, use_container_width=True)

# Lewa kolumna - 3 zdjęcia
with col_left:
    st.write("") 
    wyswietl_zdjecie_bezpiecznie("1fa08f5d77417f45981c55e8b887f909.jpg", "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("102e80d2a00f1417283bfd743d021a76.jpg", "https://images.unsplash.com/photo-1556229174-5e42a09e45af?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("9438d31b27d424e2feb4e744c7578aa3.jpg", "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?q=80&w=400")

# Prawa kolumna - 3 zdjęcia
with col_right:
    st.write("") 
    wyswietl_zdjecie_bezpiecznie("700129929a2803b16ab124197ec8ba69.jpg", "https://images.unsplash.com/photo-1608248597481-496100c8c836?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("daa4eaf344eebaaa5d8e72625ca7f976.jpg", "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?q=80&w=400")
    wyswietl_zdjecie_bezpiecznie("edf73f24d9d6a298f7d0626c20569a7c.jpg", "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400")

# Środkowa kolumna — SERCE SYSTEMU (Główny interfejs Plotkary)
with col_center:
    st.markdown('<div class="brand-logo">GlowAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-tagline">XOXO, Your Ultimate Skincare Confidant</div>', unsafe_allow_html=True)
    
    # Karta konfiguracji profilu na górze czatu
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown("<b style='color: #635252;'>Setup Twój Profil:</b>", unsafe_allow_html=True)
    c_name, c_email = st.columns(2)
    with c_name:
        user_name = st.text_input("Jak masz na imię?", value="Bff", key="user_name_input")
    with c_email:
        user_email = st.text_input("Twój e-mail (do transkrypcji):", placeholder="girl@messenger.com")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Inicjalizacja pamięci czatu (Multi-turn chat)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Cześć {user_name}! Słyszałam, że szukasz sekretu idealnej cery... Opowiedz mi, z czym dzisiaj walczy Twoja skóra? Zdradź mi wszystko! 💋"}
        ]
        
    # Wyświetlanie dymków z historii (Messenger style)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Reakcja na nową wiadomość użytkownika
    if prompt := st.chat_input("Napisz sekret o swojej skórze..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("✨ Wirtualni agenci naradzają się nad Twoim przypadkiem..."):
                odpowiedz = pytaj_agentow_czat(user_name, st.session_state.messages[:-1], prompt)
                st.markdown(odpowiedz)
        st.session_state.messages.append({"role": "assistant", "content": odpowiedz})
        
    # Przycisk do wysłania pełnej transkrypcji na maila
    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Zakończ rozmowę i wyślij cały sekret na maila 💌"):
            if not user_email or "@" not in user_email:
                st.error("💖 Podaj poprawny e-mail w panelu profilu na górze, żebym mogła wysłać wiadomość!")
            else:
                full_transcript = ""
                for msg in st.session_state.messages:
                    autor = user_name if msg["role"] == "user" else "GlowAI"
                    full_transcript += f"[{autor}]: {msg['content']}\n\n"
                
                with st.spinner("Wysyłam sekretną wiadomość..."):
                    status = send_email_transcript(user_email, user_name, full_transcript)
                    st.success(status)

# --- STOPKA NA SAMYM DOLE STRONY ---
st.markdown('<div class="brand-footer">New philosophy of selfcare: healthy skin first</div>', unsafe_allow_html=True)
